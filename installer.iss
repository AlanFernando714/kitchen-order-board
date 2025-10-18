[Setup]
AppName=KitchenOrders
AppVersion=1.0
AppPublisher=Alan_Fernando_Carlos_Flores
AppPublisherURL=https://github.com/AlanFernando714
AppSupportURL=https://github.com/AlanFernando714/kitchen-order-board/issues
AppUpdatesURL=https://github.com/AlanFernando714/kitchen-order-board/releases
DefaultDirName={autopf}\KitchenOrders
DefaultGroupName=KitchenOrders
AllowNoIcons=yes
LicenseFile=LICENSE.txt
InfoBeforeFile=README.md
OutputDir=Output
OutputBaseFilename=KitchenOrders_Installer
SetupIconFile=logo.ico
WizardStyle=modern
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
CreateAppDir=yes
Uninstallable=yes

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked


[Files]
Source: "dist\run.exe"; DestDir: "{app}"; DestName: "KitchenOrders.exe"; Flags: ignoreversion

[Icons]
Name: "{group}\KitchenOrders"; Filename: "{app}\KitchenOrders.exe"
Name: "{group}\{cm:UninstallProgram,Kitchen Orders}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\KitchenOrders"; Filename: "{app}\KitchenOrders.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\KitchenOrders.exe"; Description: "{cm:LaunchProgram,KitchenOrders}"; Flags: nowait postinstall skipifsilent
