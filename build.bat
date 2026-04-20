@echo off
rd /s /q build
rd /s /q dist
del /f /q main.spec

echo Building NUMBA_3...
python -m PyInstaller --noconfirm --onefile --windowed --icon="icon.ico" --name "NUMBA_3" --add-data "hand_landmarker.task;." main.py

echo Done!
pause