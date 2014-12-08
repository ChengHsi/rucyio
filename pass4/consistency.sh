#!/bin/bash
while read p
do
    a=`grep -rnw "tw-eos03-ls-result_adler" -e "$p"`
    if [ "$a" == "" ]
    then
        echo $p
    fi


done <venn_diagram/e_1
