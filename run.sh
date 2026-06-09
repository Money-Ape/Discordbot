#!/usr/bin/env bash
set +e
VENV_DIR="venv"

echo "=== Discord Bot Launcher ===" 

case "$(uname -s)" in # Detect Windows (Git Bash / MINGW / MSYS)
    MINGW*|MSYS*|CYGWIN*)
    WINDOWS=true
    ;;
    *)
    WINDOWS=false
    ;;
esac

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python -m venv "$VENV_DIR" # Create virtual environment if missing
fi

if [ "$WINDOWS" = true ]; then
    source "$VENV_DIR/Scripts/activate" # Activate virtual environment
else
    source "$VENV_DIR/bin/activate"
fi

python - <<'EOF' # Check dependencies
import importlib
import sys

required = [
    "discord",
    "dotenv"
]

missing = []

for module in required:
    try:
        importlib.import_module(module)
    except ImportError:
        missing.append(module)

if missing:
    print("Missing modules:", ", ".join(missing))
sys.exit(1)

sys.exit(0)
EOF

modules_missing=$?
set -e

if [ $modules_missing -ne 0 ]; then # Install dependencies if needed
    echo "Installing dependencies..."

python -m pip install --upgrade pip

pip install -U \
    discord.py \
    python-dotenv

else
    echo "All dependencies satisfied."
fi

echo "Starting bot..."
python Services/zizi.py
