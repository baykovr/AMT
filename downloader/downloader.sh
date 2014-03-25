#!/bin/sh
var=`cat input.txt`
COUNTER=1
for i in $var; do
    wget $i -O "$COUNTER.png" -P /results
	COUNTER=$[$COUNTER +1]
done