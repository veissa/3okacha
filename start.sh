#!/bin/sh
echo "Starting gunicorn on port: $PORT"
exec gunicorn --bind 0.0.0.0:"$PORT" app:app 