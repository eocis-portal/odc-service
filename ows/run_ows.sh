#!/bin/bash

conda activate odc_env

. ./ows_env.sh

flask run -h 0.0.0.0
