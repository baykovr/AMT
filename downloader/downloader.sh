#!/bin/sh
var=`cat input.txt`
for i in $var; do
    wget $i
done