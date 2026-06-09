@echo off

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

python -c "import discord, dotenv" 2>NUL

if errorlevel 1 (
    echo Installing dependencies...
    python -m pip install --upgrade pip
    python -m pip install discord.py python-dotenv
)

echo Launching PassCore...
python Services/zizi.py

pause