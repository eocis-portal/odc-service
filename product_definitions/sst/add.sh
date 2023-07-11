#!/bin/bash

TARGET_FOLDER=$1

for file in $TARGET_FOLDER/*
do
  echo $file
  datacube -C ~/.datacube_integration.conf dataset add $file
done