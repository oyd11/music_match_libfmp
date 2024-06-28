#!/usr/bin/env bash


set -u  # no unset

PORT=${1:-5001}

max_count=${2:-10}  # how many tracks to index?

counter=0

echo Running till $max_count

for f in input_audio/*.opus; do
	echo $((++counter)): $f
	curl http://127.0.0.1:$PORT/index -F file=@"$f"
	echo -----
	if [[ ${counter} -ge ${max_count} ]]; then
		echo Stopping iteration at $max_count
		break
	fi
done

