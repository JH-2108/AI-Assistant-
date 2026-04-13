Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
folder = fso.GetParentFolderName(WScript.ScriptFullName)
shell.Run "cmd /c cd /d """ & folder & """ && pythonw clap_launcher.py", 0, False