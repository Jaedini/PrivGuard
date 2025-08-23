; PrivGuard Installer Script (Full Version)
; Erstellt mit Inno Setup 6 Wizard, angepasst für PrivGuard.exe

#define MyAppName "PrivGuard"
#define MyAppVersion "1.0"
#define MyAppPublisher "Jaeden Hommel"
#define MyAppURL "https://github.com/Jaedini/PrivGuard"
#define MyAppExeName "PrivGuard.exe"
#define MyAppAssocName MyAppName + " Document"
#define MyAppAssocExt ".myp"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
AppId={{3FDC1E9C-98C1-4ECD-9975-F30A764A2808}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
ChangesAssociations=yes
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=E:\PrivGuard\LICENSE.txt
InfoBeforeFile=E:\PrivGuard\README_BEFORE.txt
InfoAfterFile=E:\PrivGuard\README_AFTER.txt
OutputBaseFilename=PrivGuard_Setup
SetupIconFile=E:\PrivGuard\favicon.ico
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Hauptprogramm
Source: "E:\PrivGuard\dist\PrivGuard.exe"; DestDir: "{app}"; Flags: ignoreversion
; Doku-Dateien
Source: "E:\PrivGuard\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\PrivGuard\README_BEFORE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\PrivGuard\README_AFTER.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\PrivGuard\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
; Optional: Ressourcen
; Source: "E:\PrivGuard\resources\*"; DestDir: "{app}\resources"; Flags: ignoreversion recursesubdirs createallsubdirs

[Registry]
; Dateityp-Verknüpfung für .myp
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

[Icons]
; Startmenü-Eintrag
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Desktop-Verknüpfung (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Programm nach der Installation starten
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
