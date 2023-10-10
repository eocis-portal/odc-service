#!/bin/bash

YEAR=$1

rsync -avrL niallmcc@xfer2.jasmin.ac.uk:/gws/nopw/j04/cds_c3s_sst/public/data/ICDR_v3/Analysis/L4/v3.0/$YEAR /data/esacci_sst/public/CDR3.0_release/Analysis/L4/v3.0.1