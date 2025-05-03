#!/bin/bash

dir="/home/roger/music/Compilations/RW's random tracks"
dir2="/home/roger/music/Public Service Broadcasting/The Race For Space"

ffmpeg -i "$dir"/Chris\ Joss\ -\ Tune\ Down.mp3 -ss 24 -t 13 -af "afade=out:st=36:d=1" clip1.mp3 -y
ffmpeg -i "$dir"/Commodores\ -\ Machine\ Gun.mp3 -t 11 -af "afade=out:st=10:d=1" clip2.mp3 -y
ffmpeg -i "$dir"/Tomoyasu\ Hotei\ -\ Battle\ Without\ Honour\ or\ Humanity.mp3 -ss 15.75 -t 5.75 clip3.mp3 -y
ffmpeg -i "$dir"/Faithless\ -\ Insomnia.mp3 -ss 137 -t 8.5 clip4.mp3 -y
ffmpeg -i "$dir"/Daft\ Punk\ -\ Get\ Lucky.mp3 -t 8.5 clip5.mp3 -y
ffmpeg -i "$dir"/BBC\ -\ Theme\ from\ Grandstand.mp3 -ss 8.5 -t 6.7 clip6.mp3 -y
ffmpeg -i "$dir"/Walter\ Murphy\ and\ the\ Big\ Apple\ Band\ -\ A\ Fifth\ Of\ Beethoven.mp3 -ss 10.2 -t 10.2 -af "afade=out:st=19.4:d=1" clip7.mp3 -y
ffmpeg -i "$dir2"/08\ -\ Go\!.mp3 -ss 72 -t 5.75 clip8.mp3 -y
