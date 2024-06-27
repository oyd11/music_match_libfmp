#!/usr/bin/env bash

PORT=${1:-5001}

set -x

curl http://127.0.0.1:$PORT/index -F file=@'input_audio/Gnarls Barkley - Crazy (Official Video) [4K Remaster] [-N4jf6rtyuw].opus'

curl http://127.0.0.1:$PORT/index -F file=@'input_audio/Boogie Down Productions - My Philosophy (Official HD Video) [h1vKOchATXs].opus'




