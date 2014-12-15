#!/bin/bash
while read line
    do
        name=$line
        echo "rucio delete-rule $name"
        /opt/rucio/.venv/bin/rucio delete-rule $name
done < $1

