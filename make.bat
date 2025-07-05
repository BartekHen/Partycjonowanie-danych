@echo off
pushd %~dp0

REM Uproszczony plik komend dla Sphinxa

set SPHINXBUILD=C:\Users\bart\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts\sphinx-build.exe
set SOURCEDIR=source
set BUILDDIR=build
set SPHINXOPTS=

if "%1" == "" (
    echo.
    echo Prosze podac typ dokumentu do zbudowania, np. "html" lub "latexpdf".
    echo Przyklad: .\make.bat html
    goto end
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%

:end
popd