@echo off
rem =====================================================================
rem  compiler.bat - compile un document LaTeX en UNE seule action.
rem
rem    Double-clic ........ compile main.tex
rem    Glisser un .tex sur ce fichier .... compile ce .tex
rem    En ligne de commande :  compiler.bat exemple-B-tp
rem                            compiler.bat nettoyer     (supprime les fichiers auxiliaires)
rem
rem  latexmk lance LuaLaTeX et Biber autant de fois que necessaire, puis
rem  ce script affiche les problemes eventuels (references manquantes,
rem  avertissements, boites trop larges) et ouvre le PDF.
rem =====================================================================
chcp 65001 >nul
setlocal
cd /d "%~dp0"

if /I "%~1"=="nettoyer" (
  latexmk -c
  echo Fichiers auxiliaires supprimes.
  goto :fin
)

set "F=%~1"
if "%F%"=="" set "F=main"
if /I "%F:~-4%"==".tex" set "F=%F:~0,-4%"

if not exist "%F%.tex" (
  echo [ERREUR] Fichier introuvable : %F%.tex
  goto :fin
)

echo.
echo === Compilation de %F%.tex  (LuaLaTeX + Biber, automatique) ===
latexmk -silent -interaction=nonstopmode "%F%.tex"
set "CODE=%ERRORLEVEL%"

echo.
echo === Verification ===
if not exist "%F%.log" (
  echo [ERREUR] Aucun journal : la compilation n'a pas demarre.
  goto :fin
)
findstr /R /C:"^!" /C:"Warning" /C:"Overfull" /C:"Underfull" /C:"Missing character" "%F%.log"
if errorlevel 1 (
  echo Aucun avertissement.
) else (
  echo ---- Voir le detail dans %F%.log
)

if not "%CODE%"=="0" (
  echo.
  echo [ECHEC] La compilation a signale une erreur : ouvrir %F%.log et chercher "!"
  goto :fin
)

echo.
echo [OK] %F%.pdf est a jour.
start "" "%F%.pdf"

:fin
echo.
if /I not "%~2"=="nopause" pause
endlocal
