#!/usr/bin/env bash


urls=( `grep "^https://" example_songs.md` )
num_urls=${#urls[@]}
echo num_urls=$num_urls

mkdir -p input_audio

pushd .
cd input_audio

for url in "${urls[@]}" ; do
	echo url=$url:
	yt-dlp -x --audio-format opus $url
	echo Done:$url:
	break
done

popd 
