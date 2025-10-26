@echo off
echo Installing Speech Recognition Dependencies...
echo ==========================================

cd backend

echo Installing Python speech recognition packages...
pip install SpeechRecognition==3.10.0
pip install PyAudio==0.2.11
pip install pocketsphinx==5.0.0

echo.
echo ✅ Speech recognition dependencies installed successfully!
echo.
echo Note: If you encounter issues with PyAudio installation on Windows,
echo you may need to install it manually from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
echo.
pause
