#!/bin/bash

dir="/home/roger/music/Compilations/RW's random tracks"
dir2="/home/roger/music/Public Service Broadcasting/The Race For Space"

ffmpeg -i "$dir"/Chris\ Joss\ -\ Tune\ Down.mp3 -ss 24.5 -t 6.5 clip1.mp3 -y
ffmpeg -i "$dir"/Rhythm\ Heritage\ -\ S.W.A.T..mp3 -ss 239.8 -t 6 -af "afade=out:st=244.75:d=1" clip2.mp3 -y
ffmpeg -i "$dir"/Tomoyasu\ Hotei\ -\ Battle\ Without\ Honour\ or\ Humanity.mp3 -ss 15.75 -t 5.75 clip3.mp3 -y
ffmpeg -i "$dir"/Faithless\ -\ Insomnia.mp3 -ss 137.8 -t 3.9 clip4.mp3 -y
ffmpeg -i "$dir"/Daft\ Punk\ -\ Get\ Lucky.mp3 -t 2.35 clip5.mp3 -y
ffmpeg -i "$dir"/BBC\ -\ Theme\ from\ Grandstand.mp3 -ss 38.85 -t 5 -af "afade=out:st=42.85:d=1" clip6.mp3 -y
ffmpeg -i "$dir"/Walter\ Murphy\ and\ the\ Big\ Apple\ Band\ -\ A\ Fifth\ Of\ Beethoven.mp3 -ss 64.7 -t 5 -af "afade=out:st=68.2:d=1" clip7.mp3 -y
ffmpeg -i "$dir2"/08\ -\ Go\!.mp3 -ss 72 -t 5.75 clip8.mp3 -y
