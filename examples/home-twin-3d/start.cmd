@echo off
cd /d "%~dp0"
echo Open http://127.0.0.1:8776/ in your browser.
python serve.py --port 8776
pause
