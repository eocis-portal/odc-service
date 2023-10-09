#!/bin/bash

START_YEAR=$1
END_YEAR=$2

for TARGET_YEAR in $(seq $START_YEAR $END_YEAR);
do
for file in $TARGET_YEAR/*
do
  echo $file
  datacube -C ~/.datacube.conf dataset add $file
done
done

