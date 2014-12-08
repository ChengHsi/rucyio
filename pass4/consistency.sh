#!/bin/bash
echo "files not in $2"
while read p
do
    a=`grep -rnw "$2" -e "$p"`
    if [ "$a" == "" ]
    then
        echo $p
    fi


done <$1
