#!/usr/bin/env bash

for f in input_audio/*.opus; do
	echo $f
	curl http://127.0.0.1:5000/index -F file=@"$f"
	echo -----
done

