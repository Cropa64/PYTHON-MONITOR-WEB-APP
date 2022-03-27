@echo off

pyinstaller.exe --onefile --runtime-tmpdir=. --hidden-import win32timezone monitor.py

if exist dist\monitor.exe (
	echo Ejecutable creado correctamente
)