Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\kanab\.gemini\antigravity\scratch\reliance_digital_checker"
WshShell.Run "python cloud_sniper.py --interval 180 --pincode 360005", 0, False
