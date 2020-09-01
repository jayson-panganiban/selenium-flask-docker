#!/bin/bash -e

if [ -f pythonbotenv/bin/activate ]; then
    echo   "Load Python virtualenv from 'pythonbotenv/bin/activate'"
    source pythonbotenv/bin/activate
fi
exec "$@"
