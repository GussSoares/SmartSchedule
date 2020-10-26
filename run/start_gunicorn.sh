#!/bin/bash

NAME="smart_event"                              #Name of the application (*)
DJANGODIR=/home/gustavo/workspace/env/SmartEvent             # Django project directory (*)
SOCKFILE=/home/gustavo/workspace/env/SmartEvent/run/gunicorn.sock        # we will communicate using this unix socket (*)
USER=gustavo                                       # the user to run as (*)
GROUP=webdata                                     # the group to run as (*)
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=smart_event.settings.production             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=smart_event.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
#source /var/www/seu_projeto/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE
