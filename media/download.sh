#!/bin/bash

MEDIAURL="benkushigian.com/musicvisualizer/media"

declare -a mpegs=("A440.mp3" 
                  "A440_With_E660_Pulse.mp3"
                  # "Noish.mp3" 
                  # "StuffnStuff.mp3" 
                  # "TicoTico.mp3" 
                  # "WesternWaltz.mp3"
                 )

declare -a wavs=( "440Hz_With_660Hz-Pulse.wav" 
                  "A1760.wav" 
                  "A3520.wav" 
                  "A440.wav"
                  "A7040.wav"
                  "A880.wav"
                  "Noish.wav"
                  "Silence.wav"
                  "StuffnStuff.wav"
                  "swing.wav"
                  "Wanks1.wav"
                  "whitenoise1.wav"
                  "whitenoise-silence.wav"
                  "WyRm.wav"
                )

# TEST IF there are no args
if [ $# -eq 0 ]; then
    echo "Must provide an argument"
    echo "    -a|--all    download all files from remote"
    echo "    -M|--mpegs  only download mp3s"
    echo "    -w|--wavs   only download wavs"
    echo "    -u|--url www.path/to/file.mp3     download file from the web"
    echo "    --clean     remove all mp3s and wavs from media/"
fi

while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -a|--all)     # Download all the things in our array
            
            for mpeg in "${mpegs[@]}"
            do
                if [ ! -f "$mpeg" ]
                then 
                    wget "$MEDIAURL/$mpeg"
                fi
            done

            for wav in "${wavs[@]}"
            do
                if [ ! -f "$wav" ]
                then 
                    wget "$MEDIAURL/$wav"
                fi
            done
            exit   # XXX: exit? Does this work?
            ;;

        
        -M|--mpegs)     # Download .mp3s
            for mpeg in "${mpegs[@]}"
            do
                if [ ! -f "$mpeg" ]
                then 
                    wget "$MEDIAURL/$mpeg"
                fi
            done
            exit
            ;;

        
        -w|--wavs)    # Download .wavs
            for wav in "${wavs[@]}"
            do
                if [ ! -f "$wav" ]
                then 
                    wget "$MEDIAURL/$wav"
                fi
            done
            exit
            echo "Exit didn't work!"
            ;;
        -u|--url)
            URL="$2"
            wget "$URL"
            shift
            ;;
        -c|--clean)
            echo "Removing all audio files"
            rm *.mp3 
            rm *.wav
            ;;
        *)  # Unknown option, exit
            echo "Unknown option $1. Exiting"
            exit
            ;;


    esac
    shift
done
