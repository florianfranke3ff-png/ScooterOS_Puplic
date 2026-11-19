# ScooterOS Firmware-Katalog

Der `firmware-index.json` ist eine **read-only** Übersicht der verfügbaren Firmware. Aktuelle ScooterOS-Versionen prüfen Updates über `ota/esp32s3-wroom1-n16r8.json`. Beide Dateien schreibt `tools/publish_lab_ota.py` aus derselben BIN, Version und Größe stimmen deshalb immer überein.

## Auswahlverfahren

- ScooterOS liest den im Firmware-Build verankerten `hardware_id` (nicht aus `bios.json` oder `vehicle.json`).
- Der ESP misst Chipfamilie, physische Flash-Größe und - sofern initialisiert - PSRAM-Größe.
- Der Katalog wird nur für exakt diese Hardware-ID durchsucht. Bei Unklarheit oder mehreren Treffern wird **kein** Update angeboten.
- Die Versionsnummer wird numerisch verglichen und ein Firmware-Eintrag nur als **Information** angezeigt. Das heruntergeladene Katalog-JSON ist **nicht signiert**.
- Unbekannte Hardwarevarianten bleiben ohne Firmware. Kein automatischer Fallback auf einen anderen ESP32-Modultyp.

## Sicherheit

Dieser Katalog enthält **keine Signatur und keinen verifizierten SHA-256-Wert**. Er ist **nicht vertrauenswürdig genug für einen Flashvorgang** und darf die OTA-Engine nicht freischalten. Für spätere Installation sind ein signiertes Release-Manifest, Verifikation von SHA-256 und Zielhardware, A/B-Rollback, verifizierter PARK-/Wartungsmodus und Sicherheitsprüfungen notwendig. Dieser Schritt installiert nichts.

Die ursprüngliche `.bin` wurde nur verschoben. WROOM-1-N16R8 braucht **Quad-Flash** und **8 MB Octal-PSRAM**. Die genaue Modulbezeichnung ist aus dem Chip allein nicht sicher auslesbar und muss beim Erstflashen anhand der Hardware feststehen.

Datei-Pfad auf GitHub: `ESP32-S3-WROOM-1/ESP32S3_N16R8/ScooterOS_ESP32S3_N16R8.bin`
