@echo off
pip install pyinstaller
pyinstaller --onefile --noconsole --name "WorkWeekClock" desktop_clock.py
echo.
echo Build complete! EXE is in the dist\ folder.
pause
