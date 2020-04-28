# SMG-UntisOfficeConverters
 
Dieses Repo liefert eine Reihe von Python-Skripts um Untis DIF Dateien in das Microsoft School-Data-Sync-CSV Format zu konvertieren. 

Diese Programme wurden für das Sebastian-Münster-Gymnasium entwickelt um möglichst schnell und effizient Office 365 einzuführen und allen Schülern einen Account bereitzustellen.
Für die Verwendung an anderen Schulen müssen ggf. Änderungen an der `untis.py` vorgenommen werden, da die Reihnfolge der Spalten innerhalb der DIF-Datei von der jeweiligen Untis-Konfiguration abhängt.

Mit `untis_sds_converter.py` können SDS-CSVs generiert werden um alle Kurszuteilungen in School-Data-Sync zu importieren.
`untis_grade_user_converter.py` generiert CSV-Tabellen zum import von neuen Nutzern im Office 365 Admin Center.
