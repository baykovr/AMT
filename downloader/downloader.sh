#!/bin/bash
COUNTER=1
while read line
do
	stringarray=($line)
	n=$(($COUNTER%5))
    wget ${stringarray[1]} -O "${stringarray[0]}$n.png" -P ./results
	COUNTER=$[$COUNTER +1]
done < $1


# for line in $var; do
# 	echo ${line[0]}
# 	# echo ${a[1]}
# 	n=$(($COUNTER%5))
#     # wget ${a[1]} -O "${a[0]}$n.png" -P ./results
# 	COUNTER=$[$COUNTER +1]

# done