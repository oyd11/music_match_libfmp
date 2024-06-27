#!/usr/bin/env bash

set -u # unbound variables - as error

DEV=${1:-false}

# cd - to be relative to 'uploads' folder
BASE_FOLDER="$(dirname "$0")"
HOTSWAP_FOLDER="../app_hotswap"
UPLOADS_FOLDER="$BASE_FOLDER/uploads"

echo Folders: BASE_FOLDER=$BASE_FOLDER , UPLOADS_FOLDER=$UPLOADS_FOLDER
cd $BASE_FOLDER

. ./venv.sh

if [ ! -d $UPLOADS_FOLDER ]; then
	if [ -d $HOTSWAP_FOLDER ]; then
		echo "Using Hotswap folder: $HOTSWAP_FOLDER"
		mkdir -p $HOTSWAP_FOLDER/uploads || exit 1
		ln -s $HOTSWAP_FOLDER/uploads uploads || exit 1
	fi # hotswap
fi # uploads did not exist

mkdir -p $UPLOADS_FOLDER/index || exit 1
mkdir -p $UPLOADS_FOLDER/query || exit 1

if [ "$DEV" == "dev" ]; then
	echo Development mode
	python3 http_app_audio/http_app_audio.py
else
	echo Release mode, using gunicorn:
	gunicorn -w 1 -b 0.0.0.0:5000 http_app_audio.http_app_audio:app

	# More than one worker only after we have shared indexing between threads..
	# gunicorn -w 4 -b 0.0.0.0:5000 http_app_audio.http_app_audio:app
fi
