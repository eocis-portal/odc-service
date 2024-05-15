#!/bin/bash

rootfolder=/home/dev/github/odc-service

rsync -avr $rootfolder/ows dev@eocis.org:/home/dev/github/odc-service
rsync -avr $rootfolder/scripts dev@eocis.org:/home/dev/github/odc-service
rsync -avr $rootfolder/src dev@eocis.org:/home/dev/github/odc-service
rsync -avr $rootfolder/setup.cfg dev@eocis.org:/home/dev/github/odc-service
rsync -avr $rootfolder/pyproject.toml dev@eocis.org:/home/dev/github/odc-service
rsync -avr $rootfolder/product_definitions dev@eocis.org:/home/dev/github/odc-service
rsync -avr $rootfolder/test dev@eocis.org:/home/dev/github/odc-service
rsync -avr $rootfolder/mapproxy dev@eocis.org:/home/dev/github/odc-service
