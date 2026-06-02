@echo off

echo.
echo Raiden 2 debug mode patch by alamone.
echo.

where python.exe >nul 2>nul
if %errorlevel% equ 0 (
  echo - Python found!
) else (
  goto errorout2
)

where nasm.exe >nul 2>nul
if %errorlevel% equ 0 (
  echo - nasm found!
) else (
  goto errorout3
)

if not exist "raiden2j/prg0.u0211" goto errorout1
if not exist "raiden2j/rom2j.u0212" goto errorout1

REM Add check for python
REM where python.exe

echo Generating Raiden 2 debug mode patch...
echo.
python combine-roms.py raiden2j/prg0.u0211 raiden2j/rom2j.u0212 r2-prg.rom
call compile2.bat
call patchit2.bat

python split-roms.py r2-prg-mod.rom raiden2j-modded/prg0.u0211 raiden2j-modded/rom2j.u0212

echo.
echo Complete.  Results in "raiden2j-modded" folder.
echo.
echo How to use the debug menu:
echo - Press 2P Start to enter the SCR debug menu.
echo - Press 2P Start again to enter the GLOBAL INFORMATION MENU.
echo - Press 1P Start to exit the current menu.

goto ending

:errorout3
echo - Error: nasm missing.
echo.
echo Please install nasm:
echo https://www.nasm.us/
goto :ending

:errorout2
echo - Error: python missing.
echo.
echo Please install Python:
echo https://apps.microsoft.com/detail/9pnrbtzxmb4z
goto :ending

:errorout1
echo - Error: missing rom files.
echo.
echo Please copy Raiden 2 "prg0.u0211" and "rom2j.u0212" into the "raiden2j" folder and try again.
goto :ending

:ending
echo.
pause
