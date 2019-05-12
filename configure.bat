for %%I in (%~dp0\.) do set CurrDirName=%%~nxI
set AppDir=%~dp0
pip install -U --user virtualenv
virtualenv --no-site-packages %AppDir%
call %AppDir%\Scripts\activate.bat & pip install -r %AppDir%\requirements.txt
