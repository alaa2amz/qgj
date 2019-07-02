#! /bin/bash
db_name="jm4.db"
jm_xml="sources/JMdict"
jm_schema="jm-schema.txt"

if [[ -f "$db_name" ]]
   then
       rm "$db_name"
fi

./schema-sqliter.py "$jm_schema" "$db_name"
./jm-parser.py "$jm_xml" "$db_name"


