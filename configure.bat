for %%I in (%~dp0\.) do set CurrDirName=%%~nxI
set AppDir=%~dp0
pip3 install -U --user virtualenv
python3 -m virtualenv --no-site-packages %AppDir%
call %AppDir%\Scripts\activate.bat & pip install -r %AppDir%\requirements.txt
