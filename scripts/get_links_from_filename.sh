#!/bin/bash

while getopts f:l: option
do
case "${option}"
in
f) FILE_NAMES=${OPTARG};;
l) FILE_LINKS=${OPTARG};;
esac
done

echo $FILE_NAMES
cat $FILE_NAMES | while read line
do
    grep $line $FILE_LINKS >> output.txt
done

# while read p; do
#   echo "$p"
# done < $FILE_NAMES
