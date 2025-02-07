#!/bin/bash
NAME="eventos"
PATHHOME="/home/dev2/eventos"
PATHENV="$PATHHOME/env"
PATHDJANGO="$PATHHOME"
USER="dev2"
GROUP="dev2"
WORKERS=3
DJANGOWSGI="eventos.wsgi"
IP=192.168.***.***
PORT=8030
LEVEL="debug"
echo "Starting App Eventos"
source $PATHENV/bin/activate
cd $PATHDJANGO

exec gunicorn $DJANGOWSGI --bind=$IP:$PORT --workers=$WORKERS --user=$USER --group=$GROUP --log-level=$LEVEL