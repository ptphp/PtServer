[Setup]
AppId={{88B330D8-B45E-4CFE-A0FC-DA690A4570B5}
AppName=PtServer
AppVerName=PtServer V1.0
AppPublisher=PtPHP
AppPublisherURL=http://www.ptphp.com/
AppSupportURL=http://www.ptphp.com/
AppUpdatesURL=http://www.ptphp.com/
DefaultDirName=C:\PtServer
UsePreviousAppDir=yes
DefaultGroupName=PtServer
AllowNoIcons=yes
OutputBaseFilename=PtServer-1.0.2
Compression=lzma
SolidCompression=yes

[Languages]
Name: "chinese"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]

;Source: "E:\workspace\PtServer\dist\App.exe"; DestDir: "{app}"; Flags: ignoreversion
;Source: "E:\workspace\PtServer\dist\imageformats\*"; DestDir: "{app}\imageformats"; Flags: ignoreversion recursesubdirs createallsubdirs

Source: "D:\PtServer\dist\config.cfg"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\PtServer\dist\var/data/mysql/mysql.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\PtServer\dist\App.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\PtServer\dist\w9xpopen.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\PtServer\dist\imageformats\*"; DestDir: "{app}\imageformats"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\PtServer\dist\Microsoft.VC90.CRT\*"; DestDir: "{app}\Microsoft.VC90.CRT"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\PtServer\dist\var\res\*"; DestDir: "{app}\var\res"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\PtServer\dist\var\www\*"; DestDir: "{app}\var\www"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\PtServer\dist\etc\nginx_win\*"; DestDir: "{app}\etc\nginx_win"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\PtServer\dist\etc\php53_win\*"; DestDir: "{app}\etc\php53_win"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\PtServer\dist\usr\bin\*"; DestDir: "{app}\usr\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\PtServer\dist\usr\local\php\53\*"; DestDir: "{app}\usr\local\php\53"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\PtServer\dist\usr\local\mysql\*"; DestDir: "{app}\usr\local\mysql"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\PtServer\dist\usr\local\nginx\*"; DestDir: "{app}\usr\local\nginx"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\PtServer\dist\usr\local\openssl\*"; DestDir: "{app}\usr\local\openssl"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\PtServer\dist\usr\local\memcached\*"; DestDir: "{app}\usr\local\memcached"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\PtServer\dist\usr\local\mongodb\*"; DestDir: "{app}\usr\local\mongodb"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\PtServer\dist\usr\local\ssdb-bin\*"; DestDir: "{app}\usr\local\ssdb-bin"; Flags: ignoreversion recursesubdirs createallsubdirs


[Icons]
Name: "{group}\PtServer"; Filename: "{app}\App.exe"
Name: "{group}\{cm:ProgramOnTheWeb,PtServer}"; Filename: "http://www.ptphp.com/"
Name: "{group}\{cm:UninstallProgram,PtServer}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\PtServer"; Filename: "{app}\App.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\PtServer"; Filename: "{app}\App.exe"; Tasks: quicklaunchicon


[Run]
Filename: "{app}\App.exe"; Description: "{cm:LaunchProgram,PtServer}"; Flags: nowait postinstall skipifsilent