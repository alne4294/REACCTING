#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Error! - Example of correct usage: $>sh run_import_pems.sh <dir_of_.csv_files> <collection_name> "
    exit 1
fi

for file in `find $1 -name "*.csv"`
do
 echo "------------------------------"
 echo "Processing $file"
 #Import all files in directory with ext .csv
 ruby import_pems.rb $file $2
done