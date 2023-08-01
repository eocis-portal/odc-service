#!/bin/bash

rootfolder=/home/dev/github/odc-service

rsync -avr $rootfolder/ows dev@192.171.169.123:/home/dev/github/odc-service
rsync -avr $rootfolder/scripts dev@192.171.169.123:/home/dev/github/odc-service
rsync -avr $rootfolder/src dev@192.171.169.123:/home/dev/github/odc-service
rsync -avr $rootfolder/setup.cfg dev@192.171.169.123:/home/dev/github/odc-service
rsync -avr $rootfolder/pyproject.toml dev@192.171.169.123:/home/dev/github/odc-service
rsync -avr $rootfolder/product_definitions dev@192.171.169.123:/home/dev/github/odc-service
rsync -avr $rootfolder/test dev@192.171.169.123:/home/dev/github/odc-service
