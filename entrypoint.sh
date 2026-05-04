#!/bin/bash
set -e

if ! pgrep -x Xvfb > /dev/null 2>&1; then
    Xvfb :99 -screen 0 1920x1080x24 -nolisten tcp &
    sleep 0.5
fi

export DISPLAY=:99
exec "$@"
