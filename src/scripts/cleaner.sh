#!/bin/bash
dir = src
echo cleaning...

cd -- '$dir'

echo removing wav file

rm def_output.wav

echo removing output.ly
rm output.ly

echo removing output.pdf
rm output.pdf

echo removing output.log
rm output.log

echo cleaner done
