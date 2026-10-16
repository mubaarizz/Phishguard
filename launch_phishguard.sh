#!/bin/bash
cd "$HOME/Phishguard" || exit 1
source .venv/bin/activate
python -m flask --app app.web run --debug &
SERVER_PID=$!
trap 'kill "$SERVER_PID" 2>/dev/null' EXIT INT TERM
sleep 2
xdg-open http://127.0.0.1:5000
wait "$SERVER_PID"
