#!/usr/bin/env python3
"""Publish a one-file ScooterOS OTA release for NON-DRIVABLE LAB devices only.

User only uploads ScooterOS.bin to this public repository. GitHub Actions
validates the ESP-IDF image and generates the legacy LAB filename and manifest
expected by already-flashed scooteros_s3_unsigned_ota_test devices.

Never use these unsigned releases on a vehicle with connected motor control.
The production OTA channel remains separately signature-verified.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

SOURCE = Path("ScooterOS.bin")
LAB_BIN = Path("ESP32-S3-WROOM-1/ESP32S3_N16R8/ScooterOS_ESP32S3_N16R8_LAB.bin")
MANIFEST = Path("ota/esp32s3-wroom1-n16r8-lab.json")
LAB_URL = (
    "https://raw.githubusercontent.com/florianfranke3ff-png/ScooterOS_Puplic/"
    "main/ESP32-S3-WROOM-1/ESP32S3_N16R8/ScooterOS_ESP32S3_N16R8_LAB.bin"
)
APP_DESC_MAGIC = bytes.fromhex("3254cdab")
MAX_OTA_SIZE = 0x600000  # Each ESP32-S3 N16R8 OTA app slot: 6 MiB


def read_app_descriptor(blob: bytes) -> tuple[str, str]:
    if not 256 <= len(blob) <= MAX_OTA_SIZE:
        raise ValueError("Firmware does not fit the 6 MiB ESP32-S3 OTA slot")
    if blob[0] != 0xE9:
        raise ValueError("Not an ESP-IDF application image (magic 0xE9 missing)")
    offset = blob.find(APP_DESC_MAGIC, 24, 256)
    if offset == -1 or offset + 80 > len(blob):
        raise ValueError("ESP-IDF application descriptor not found")
    try:
        version = blob[offset + 16 : offset + 48].split(b"\0", 1)[0].decode("ascii")
        project = blob[offset + 48 : offset + 80].split(b"\0", 1)[0].decode("ascii")
    except UnicodeDecodeError as exc:
        raise ValueError("Invalid ESP-IDF application descriptor") from exc
    if not re.fullmatch(r"\d{1,4}\.\d{1,4}\.\d{1,4}", version):
        raise ValueError(f"Invalid embedded firmware version: {version!r}")
    if project != "scooteros":
        raise ValueError(f"Unexpected ESP-IDF project: {project!r}")
    return version, project


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit("Upload ScooterOS.bin to the repository root first")
    blob = SOURCE.read_bytes()
    version, _ = read_app_descriptor(blob)

    # Existing 0.1.1 lab firmware pins THIS exact LAB download URL. Keeping the
    # generated filename and manifest URL avoids reflashing the test ESP32.
    LAB_BIN.parent.mkdir(parents=True, exist_ok=True)
    LAB_BIN.write_bytes(blob)

    release = {
        "project": "ScooterOS",
        "board": "esp32s3-wroom1-n16r8",
        "chip": "ESP32-S3",
        "version": version,
        "channel": "lab",
        "size": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
        "url": LAB_URL,
        "test_only": True,
        "warning": "UNSIGNED OTA LABORATORY TEST; NO CONNECTED DRIVETRAIN",
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
    print(f"Published lab OTA version={version} size={len(blob)} sha256={release['sha256']}")


if __name__ == "__main__":
    main()
