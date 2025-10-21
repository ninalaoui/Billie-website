@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting song download...
python download_songs.py

echo.
echo Done! Press any key to exit...
pause
