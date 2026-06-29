Set WshShell = CreateObject("WScript.Shell")
' Replace the path below with the exact folder path where your downloader.py is saved
WshShell.Run "python C:\YouTubeDownloader\downloader.py", 0, false
