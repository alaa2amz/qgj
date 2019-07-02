#! /bin/bash
db_name="kd4.db"
kd_xml="sources/kanjidic2.xml"
kd_schema="kd-schema.txt"
krad1="sources/kradfile_utf8"
krad2="sources/kradfile2_utf8"
krad213="krad_213.txt"

if [[ -f "$db_name" ]]
   then
       rm "$db_name"
fi

./schema-sqliter.py "$kd_schema" "$db_name"
./kd-parser.py "$kd_xml" "$db_name"
./krad-parser.py "$krad1" "$db_name"
./krad-parser.py "$krad2" "$db_name"
./insert-12-parts-into-literal.py  "$db_name"
./replace-holders.py "$db_name"
./krad-parser.py "$krad213" "$db_name"



