#!/bin/bash
# USAGE: bash compare.sh filelist1 filelist2
# This is Shitty
echo "files not in $2"
while read p
do
    a=`grep -rnw "$2" -e "$p"`
    if [ "$a" == "" ]
    then
        echo $p
    fi


done <$1
