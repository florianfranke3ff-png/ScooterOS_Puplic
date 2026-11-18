# ScooterOS Fahrzeugprofil: WebUI/App-Rechte pro Einstellung

**Entwurfsstatus:** Dieses Profil enthält vorbereitete OEM-Berechtigungen.
Die aktuell veröffentlichte ScooterOS-BIN wertet diese Rechte noch nicht
vollständig im WebUI und in den Schreib-APIs aus. Keine Motorfreigabe.

Die `vehicle.json` erhält `settings_access.rules`:

- `available`: Fahrzeugentwickler bietet diese Einstellung an. **Kein**
  Nachweis für eine angeschlossene Hardware/kompilierten Treiber.
- `webui.visible`: Einstellung im WebUI anzeigen.
- `webui.editable`: Änderung durch den Endnutzer im WebUI anbieten.
- `app.visible`: Einstellung in der späteren App anzeigen.
- `app.editable`: Änderung durch den Endnutzer in der App anbieten.

`enabled` am eigentlichen Feature ist unabhängig: `vesc.enabled: false`
bedeutet weiterhin, dass der VESC nicht aktiviert ist. Die physische
Pin-/Treiberzuordnung kommt unverändert aus `bios.json`.

Die neuen Stromfelder in `vesc.limits`, `battery.limits` sowie in
`ride_modes.modes[].limits` verwenden **Ampere**, der Geschwindigkeitswert
`speed_limit_kmh` **km/h**. `null` bedeutet „nicht konfiguriert“,
**nicht** „unbegrenzt“. Batteriestrom ist der Strom des gemeinsamen Akkupacks,
Motorstrom der Strom pro Motorcontroller.

**Herstellervorgabe:** Motorstrom/Batteriestrom im WebUI und in der App
sichtbar, jedoch nicht für Endnutzer editierbar. Fahrstufennamen dürfen
geändert werden. Diese Vorgaben sind derzeit nur Metadaten, keine
manipulationssichere Herstellersperre.

Die aktive Konfiguration soll zukünftig vollständig in `vehicle.json`
leben, die WLAN-Netze bleiben separat in `wifi.json`. Eine `vesc.json`
ist nicht vorgesehen. Vor einer Freigabe müssen das aktuelle VESC-WebUI
(`/user/vesc_control.json`), die Batterie-Overrides und sämtliche
Backend-Schreibzugriffe migriert und validiert werden.
