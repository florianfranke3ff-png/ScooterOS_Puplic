#!/usr/bin/env python3
"""ScooterOS single-BIN publishing, non-drivable development hardware ONLY.

Upload a single image to:
ESP32-S3-WROOM-1/ESP32S3_N16R8/ScooterOS_ESP32S3_N16R8.bin

The release manifest for new ScooterOS versions always points to this
normal filename. A ONE-TIME compatibility copy/manifest is produced for
firmware 0.1.4, enabling existing 0.1.3 boards (which hard-code the _LAB
filename) to update over Wi-Fi. Version 0.1.5+ drops the old _LAB alias.

Not signed: NEVER use with connected motors, actuators or a drivable HCU.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path("ESP32-S3-WROOM-1/ESP32S3_N16R8")
IMAGE = ROOT / "ScooterOS_ESP32S3_N16R8.bin"
LEGACY_IMAGE = ROOT / "ScooterOS_ESP32S3_N16R8_LAB.bin"
MANIFEST = Path("ota/esp32s3-wroom1-n16r8.json")
CATALOG = Path("firmware-index.json")  # informational overview, same BIN
HARDWARE_ID = "esp32s3-wroom1-n16r8"
LEGACY_MANIFEST = Path("ota/esp32s3-wroom1-n16r8-lab.json")
BASE_URL = ("https://raw.githubusercontent.com/"
            "florianfranke3ff-png/ScooterOS_Puplic/main/"
            "ESP32-S3-WROOM-1/ESP32S3_N16R8/")
IMAGE_URL = BASE_URL + IMAGE.name
LEGACY_URL = BASE_URL + LEGACY_IMAGE.name
APP_DESC_MAGIC = bytes.fromhex("3254cdab")
MAX_OTA_SIZE = 0x600000


def app_version(data: bytes) -> str:
    if not 256 <= len(data) <= MAX_OTA_SIZE:
        raise ValueError("BIN does not fit the ESP32-S3 N16R8 OTA partition")
    if data[0] != 0xE9:
        raise ValueError("Not a valid ESP-IDF application image")
    off = data.find(APP_DESC_MAGIC, 24, 256)
    if off < 0 or off + 80 > len(data):
        raise ValueError("Missing ESP-IDF application descriptor")
    try:
        version = data[off + 16:off + 48].split(b"\0", 1)[0].decode("ascii")
        project = data[off + 48:off + 80].split(b"\0", 1)[0].decode("ascii")
    except UnicodeError as exc:
        raise ValueError("Invalid ESP-IDF descriptor") from exc
    if not re.fullmatch(r"\d{1,4}\.\d{1,4}\.\d{1,4}", version):
        raise ValueError(f"Invalid firmware version {version!r}")
    if project != "scooteros":
        raise ValueError(f"Unexpected project {project!r}")
    return version


def build_manifest(data: bytes, version: str, url: str) -> dict:
    return {
        "project": "ScooterOS",
        "board": "esp32s3-wroom1-n16r8",
        "chip": "ESP32-S3",
        "version": version,
        "channel": "lab",  # transport/dev only, no signature trust
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "url": url,
        "test_only": True,
        "warning": "UNSIGNED DEVELOPMENT OTA; NO CONNECTED DRIVETRAIN",
    }


def write_manifest(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def update_catalog(version: str, size: int) -> None:
    """Keep firmware-index.json in step with the OTA manifest.

    Both files describe the same BIN; before this, only the manifest was
    written and the catalog fell behind (0.1.1 next to a 0.1.6 image).
    """
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = [r for r in catalog.get("releases", []) if r.get("hardware_id") == HARDWARE_ID]
    if len(entries) != 1:
        raise SystemExit(f"{CATALOG}: expected exactly one release for {HARDWARE_ID}")
    entries[0]["version"] = version
    entries[0]["firmware_size_bytes"] = size
    entries[0]["test_note"] = ("Nur Information, keine Installation. Version und Groesse stammen aus der "
                               "verlinkten BIN; Updates prueft ScooterOS ueber " + str(MANIFEST) + ".")
    CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    if not IMAGE.is_file():
        raise SystemExit(f"Upload the new BIN to {IMAGE} first")
    data = IMAGE.read_bytes()
    version = app_version(data)
    major, minor, patch = (int(v) for v in version.split("."))
    if (major, minor, patch) < (0, 1, 4):
        # Updating this workflow must not republish or invalidate the last
        # already-working 0.1.3 release while no new BIN has been uploaded.
        print("Existing 0.1.3 image detected. No new release to publish.")
        return
    write_manifest(MANIFEST, build_manifest(data, version, IMAGE_URL))
    update_catalog(version, len(data))

    # The old 0.1.3 firmware has the LAB path hard-coded. A bridge release is
    # unavoidable if we want a seamless transition without a USB reflash.
    if (major, minor, patch) == (0, 1, 4):
        LEGACY_IMAGE.write_bytes(data)
        write_manifest(LEGACY_MANIFEST,
                       build_manifest(data, version, LEGACY_URL))
        print("Bridge release: old boards can OTA to 0.1.4 using old LAB URL.")
    else:
        # After the 0.1.4 transition, stop publishing the legacy BIN.
        LEGACY_IMAGE.unlink(missing_ok=True)
        LEGACY_MANIFEST.unlink(missing_ok=True)
        print("Normal OTA path only; legacy LAB firmware/manifest removed.")

    print(f"ScooterOS {version}: {len(data)} bytes; "
          f"SHA-256 {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
