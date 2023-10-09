#! /usr/bin/env bash

#
# Caution: ensure child products are removed first
#

PRODUCT_NAME=$1

conda activate odc_env

export DB_DATABASE=odc
export DB_HOSTNAME=localhost
export DB_USERNAME=dev

read -p "Are you sure you want to delete product ${PRODUCT_NAME}? (Y to continue): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1
fi

# Delete from OWS
psql -U $DB_USERNAME -d $DB_DATABASE -h $DB_HOSTNAME \
  -f delete_odc_product_ows.sql -v product_name=$PRODUCT_NAME

# Delete from ODC
psql -U $DB_USERNAME -d $DB_DATABASE -h $DB_HOSTNAME \
  -f delete_odc_product.sql -v product_name=$PRODUCT_NAME

# Clean up ODC indexes
psql -U $DB_USERNAME -d $DB_DATABASE -h $DB_HOSTNAME \
  -f cleanup_odc_indexes.sql -v product_name=$PRODUCT_NAME
