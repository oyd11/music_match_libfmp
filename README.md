
Playing with Musical Fingerprints, With the Jupyter notebooks provided at:


https://www.audiolabs-erlangen.de/resources/MIR/FMP/C7/C7S1_AudioIdentification.html



## Running server in Docker

```bash
```

## Installing locally

```bash
. ./mk_venv.sh  # create expected env
. ./venv.sh     # activate virtual-env


```


```bash
✗ ./index_example.sh 5000  # index example files, to port 5000, or 5001 in the Docker example
+ curl http://127.0.0.1:5000/index -F 'file=@input_audio/Gnarls Barkley - Crazy (Official Video) [4K Remaster] [-N4jf6rtyuw].opus'
{
  "info": {
    "Fs": 22050,
    "bin_sec": 0.046439909297052155,
    "duration_sec": 180.61351473922903,
    "n_fft": 2048,
    "n_hop": 1024
  },
  "message": "File successfully uploaded to Gnarls_Barkley_-_Crazy_Official_Video_4K_Remaster_-N4jf6rtyuw.opus"
}
+ curl http://127.0.0.1:5001/index -F 'file=@input_audio/Boogie Down Productions - My Philosophy (Official HD Video) [h1vKOchATXs].opus'
{
  "info": {
    "Fs": 22050,
    "bin_sec": 0.046439909297052155,
    "duration_sec": 299.57351473922904,
    "n_fft": 2048,
    "n_hop": 1024
  },
  "message": "File successfully uploaded to Boogie_Down_Productions_-_My_Philosophy_Official_HD_Video_h1vKOchATXs.opus"
}

✗ ./query_example.sh 5000
{
  "choice": [
    "Gnarls_Barkley_-_Crazy_Official_Video_4K_Remaster_-N4jf6rtyuw",
    18.250884353741498,
    38
  ],
  "message": "File successfully uploaded to crazy_ph_part.mp3",
  "stats": [
    [
      38,
      18.250884353741498,
      "Gnarls_Barkley_-_Crazy_Official_Video_4K_Remaster_-N4jf6rtyuw"
    ],
    [
      12,
      117.3536507936508,
      "Boogie_Down_Productions_-_My_Philosophy_Official_HD_Video_h1vKOchATXs"
    ]
  ]
}
```
