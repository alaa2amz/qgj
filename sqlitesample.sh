#! /bin/bash

db_name="$1"
no_of_lines=${2:-5}

for x in `sqlite3 $db_name ".tables"`;
do
    echo -e "\n|->table $x\n";
    sqlite3 $db_name  -nullvalue NULL -header "select * from $x limit $no_of_lines";
done
