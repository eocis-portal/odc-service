#!/bin/bash

TARGET_FOLDER=$1
START_YEAR=$2
END_YEAR=$3

for year in `seq $START_YEAR $END_YEAR`
do
  folder=$TARGET_FOLDER/$year
  for file in $folder/*
  do
    echo $file
    datacube -C ~/.datacube.conf dataset add $file
  done
done
