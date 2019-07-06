#!/bin/sh
source venv/bin/activate
flask db upgrade
exec gunicorn --certfile cert.pem --keyfile key.pem -b 80:5000 --access-logfile - --error-logfile - application:application
