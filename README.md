# ScooterOS – Firmware-Downloads

Dieses öffentliche Repository enthält Firmware-Artefakte, nach ESP32-Modul und Speichervariante getrennt.

## Ordner

- [ESP32](ESP32/) – klassischer ESP32 (noch keine Firmware veröffentlicht).
- [ESP32-S3-WROOM-1](ESP32-S3-WROOM-1/) – ESP32-S3-WROOM-1, nach Flash-/PSRAM-Variante.
- [ESP32-S3-WROOM-2](ESP32-S3-WROOM-2/) – ESP32-S3-WROOM-2 (andere Flash-Anbindung, nicht mit WROOM-1 gleichsetzen).

## Wichtige Hinweise

1. **Nur die zur Hardware passende Firmware flashen.** Chipfamilie, exakter Modultyp, Flash-Modus und -Größe, PSRAM sowie Partitionstabelle müssen stimmen.
2. Eine `.bin` für ein Board ist nicht automatisch auf einem anderen Board verwendbar. Ein eigener Build ist dann nötig, wenn sich relevante Hardware-/Build-Parameter unterscheiden.
3. Für mehrere Controller **derselben Hardwareklasse** kann die gleiche ScooterOS-Firmware eingesetzt werden. Fahrzeug-/Boardrollen (z. B. GT2 Master und Slave) werden separat über `bios.json` und `vehicle.json` konfiguriert.
4. Der feste Firmware-Dateiname wird für Updates beibehalten; Git speichert alte Stände in der Commit-Historie.
5. **Aktuell ist OTA in ScooterOS nicht freigeschaltet.** Die Datei hier ist noch kein automatisch installierbares, signiertes OTA-Release.
6. Für eine Erstinstallation können zusätzlich Bootloader und Partitionstabelle nötig sein. Vor dem Flashen die konkrete Hardware und das Ziel-Layout verifizieren.

**Sicherheit:** ScooterOS befindet sich noch in der Entwicklung. Nicht als fahrfähige Steuerungs-Firmware einsetzen, solange Fahrzeug- und OTA-Sicherheitsfunktionen nicht geprüft und freigegeben sind.
