#!/usr/bin/env bash

PORT=${1:-5001}

curl http://127.0.0.1:$PORT/query -F file=@'input_audio/phoneSpeakerInRoom/crazy_ph_part.mp3'    


