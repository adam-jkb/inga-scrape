#!/bin/sh
# encoding: utf-8

if [ $# -gt 2 ] || [ $# -lt 1 ]; then
	echo "invalid number of parameters"
	exit 1
fi

if ! [ -f "$1" ]; then
	echo "invalid input file"
	exit 1
fi

if [ $# -eq 1 ] || [ "$1" = "$2" ]; then
	OUTPUT="$1"
else 
	OUTPUT="$2"
fi
UA=$(cat $1 | grep Mozilla/)
START=$(cat $1)
echo "$1" | grep -q "ff" && START=$(sed 's/: /:\n/g' $1)
DEDUPE=$(echo "$START" | sed 's/"/\\"/g' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\\"\n/\\""\n/g')
SEDD=$(echo "$DEDUPE" |  sed -e ':a' -e 'N' -e '$!ba' -e 's/:\n/": "\n/g' | sed -e ':a' -e 'N' -e '$!ba' -e 's/"\n/"/g' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/"\n"/g' | sed 's/""/""\n"/g')
STARTL=$(echo "\t\"$SEDD")
COMMAS=$(echo "$STARTL" | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/,\n\t/g' )
#COMMENT="$COMMAS"
COMMENT=$(echo "$COMMAS" | sed 's/"cookie":/#"cookie":/g' | sed 's/"Cookie":/#"Cookie":/g' | sed 's/"Connection":/#"Connection":/g' | sed 's/"connection":/#"connection":/g')

echo "#!/usr/bin/env python" > "$OUTPUT"
echo "# encoding: utf-8" >> "$OUTPUT"
echo "DEFAULT_REQUEST_HEADERS = {" >> "$OUTPUT"

echo "$COMMENT\"" >> "$OUTPUT"

echo "}" >> "$OUTPUT"
echo "USER_AGENT = '$UA'" >> "$OUTPUT"
