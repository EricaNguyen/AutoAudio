#!/bin/bash
echo creating pdf, wait a minute...
lilypond output.ly
echo pdf done

echo moving pdf to folder

mkdir ~/Desktop/AutoAudioOutput
mv output.pdf ~/Desktop/AutoAudioOutput