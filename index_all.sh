#!/usr/bin/env bash

PORT=${1:-5001}

for f in input_audio/*.opus; do
	echo $f
	curl http://127.0.0.1:$PORT/index -F file=@"$f"
	echo -----
done

