#!/bin/bash

while getopts f: option
do
case "${option}"
in
f) FOLDER=${OPTARG};;
esac
done

FOLDER=$(printf %q "$FOLDER")

find $FOLDER -type f -name '*.pdf.0' | while read f; do mv "$f" "${f%.0}"; done
