#!/bin/bash
# Install dependencies, set up autorun, and start the assistant
set -e
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Add @reboot entry to current user's crontab if missing
if ! crontab -l 2>/dev/null | grep -q "# SamanthaAssistantAutorun"; then
    (crontab -l 2>/dev/null; echo "@reboot $BASE_DIR/venv/bin/python $BASE_DIR/rag_assistant.py") | crontab -
    echo "Added reboot entry to crontab"
fi

exec "$BASE_DIR/venv/bin/python" rag_assistant.py
