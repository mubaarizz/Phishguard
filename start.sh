#!/bin/bash
cd "$HOME/Phishguard" || exit 1

if ! curl -fsS http://127.0.0.1:5000/ >/dev/null 2>&1; then
    nohup ./.venv/bin/python -m flask --app app.web run --no-debugger \
        > /tmp/phishguard-flask.log 2>&1 < /dev/null &
    for i in {1..15}; do
        curl -fsS http://127.0.0.1:5000/ >/dev/null 2>&1 && break
        sleep 1
    done
fi

xdg-open http://127.0.0.1:5000/
