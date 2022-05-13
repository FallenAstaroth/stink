@echo on & set /P file="File name for compilation (for example test.py): " & set /P compression="Compress the file? (y/n): " & set /P console="Disable console? (y/n): "

pip install virtualenv & virtualenv venv & call venv\Scripts\activate

pip install -r requirements.txt & pip install Nuitka==0.6.16.4 & if "%compression%" == "y" (pip install zstandard==0.17.0) else (echo Y|pip uninstall zstandard)

if "%console%" == "y" (
    nuitka --onefile --windows-disable-console %file%
) else (
    nuitka --onefile %file%
)

pause