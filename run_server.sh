#!/usr/bin/env bash

set -u # unbound variables - as error

# Set the default port if not provided
PORT=${1:-13337}
DEV=${2:-false}


# cd - to be relative to 'uploads' folder
BASE_FOLDER="$(dirname "$0")"
HOTSWAP_FOLDER="../app_hotswap"
UPLOADS_FOLDER="$BASE_FOLDER/uploads"

echo FOlders: $BASE_FOLDER , $UPLOADS_FOLDER
cd $BASE_FOLDER

. ./venv.sh


if [ -d $HOTSWAP_FOLDER ]; then
     echo "Using Hotswap folder: $OUT_FOLDER"
     mkdir -p $HOTSWAP_FOLDER/uploads || exit 1
     ln -s $HOTSWAP_FOLDER/uploads uploads || exit 1
fi

mkdir -p $UPLOADS_FOLDER/index || exit 1
mkdir -p $UPLOADS_FOLDER/query || exit 1

if [ "$DEV" == "dev" ]; then
	echo Development mode
	python http_app_audio/http_app_audio.py
else
	echo Release mode, using gunicorn:
	gunicorn -w 4 -b 0.0.0.0:$PORT http_app_audio.http_app_audio:app
fi



