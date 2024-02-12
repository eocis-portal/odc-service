#/bin/bash

. `dirname $0`/settings.sh

##############################

echo stopping database

pg_ctl -D $DATABASE_PATH -l $DATABASE_PATH/log.log stop

if [ ! -d $BACKUP_DATABASE_PATH ];
then
   echo No backup found at $BACKUP_DATABASE_PATH to restore from
else
   echo restoring $BACKUP_DATABASE_PATH => $DATABASE_PATH
   rm -Rf $DATABASE_PATH
   cp -r $BACKUP_DATABASE_PATH $DATABASE_PATH
fi

echo restarting database

pg_ctl -D $DATABASE_PATH -l $DATABASE_PATH/log.log start

