#/bin/bash

. `dirname $0`/settings.sh

##############################

echo stopping database

pg_ctl -D $DATABASE_PATH -l $DATABASE_PATH/log.log stop

if [ -d $BACKUP_DATABASE_PATH ];
then
   echo Removing previous backup $BACKUP_DATABASE_PATH
   echo rm -Rf $BACKUP_DATABASE_PATH
fi

echo backing up $DATABASE_PATH to $BACKUP_DATABASE_PATH
cp -r $DATABASE_PATH $BACKUP_DATABASE_PATH

echo restarting database

pg_ctl -D $DATABASE_PATH -l $DATABASE_PATH/log.log start

