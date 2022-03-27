@echo off

pyinstaller.exe --onefile --windowed --icon "C:\Users\messi\Documents\Curso programacion\Python\monitoreoWeb\MONITOR APP\eyeReduced.ico" --runtime-tmpdir=. --hidden-import win32timezone monitorApp.py

if exist dist\monitorApp.exe (
	echo Ejecutable creado correctamente
) else (
	echo Error al crear ejecutable
)