@echo off
setlocal enabledelayedexpansion
set total_duration=0

for %%f in (*.mp4) do (
    for /f "tokens=2 delims=,." %%a in ('ffmpeg -i "%%f" 2>&1 ^| findstr /C:"Duration"') do (
        set duration=%%a
        set /a hours=duration:~0,2, minutes=duration:~3,2, seconds=duration:~6,2
        set /a file_duration=(hours*3600)+(minutes*60)+seconds
        set /a total_duration+=file_duration
    )
)

set /a hours=total_duration/3600
set /a minutes=(total_duration%3600)/60
set /a seconds=total_duration%60

echo Total Duration: %hours%:%minutes%:%seconds% > total_duration.txt
endlocal