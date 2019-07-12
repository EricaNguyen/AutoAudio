#!/bin/bash
echo running program...

./cleaner.sh

echo running freqAnalyzer..
python3 freqAnalyzer.py

echo creating pdf, wait a minute...
lilypond output.ly
echo pdf done

echo moving pdf to folder

mkdir ~/Desktop/AutoAudioOutput
mv output.pdf ~/Desktop/AutoAudioOutput

echo CleanAndRun done
