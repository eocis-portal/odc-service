#/bin/bash

. `dirname $0`/settings.sh

initdb -D $DATABASE_PATH

##############################

pg_ctl -D $DATABASE_PATH -l $DATABASE_PATH/log.log start

createdb --owner=$USERNAME $DBNAME

pg_ctl -D $DATABASE_PATH -l $DATABASE_PATH/log.log stop
