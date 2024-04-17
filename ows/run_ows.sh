#!/bin/bash

conda activate odc_env

. ./ows_env.sh

nohup flask run >> /dev/null &
