@echo off
SETLOCAL

SET "StatusFile=setings.txt"
SET "InstallFlag="
FOR /F "tokens=2" %%A IN (%StatusFile%) DO (
    SET "InstallFlag=%%A"
    GOTO CheckFlag
)
:CheckFlag
IF "%InstallFlag%" EQU "0" (
    %CD%\.venv\Scripts\python.exe mesenger_install.py
)
ENDLOCAL
 %CD%\.venv\Scripts\python.exe mesenger_client.py