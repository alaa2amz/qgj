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

sqlite3 $db_name   "insert into kpt(literal_id,pt__literal_id) select k_parts.literal_id, literal.literal_id from k_parts,literal,parts where k_parts.parts_id =parts.parts_id and literal.literal_value = parts.parts_value;"

sqlite3 $db_name "CREATE VIEW kanji_part(kanji,part) AS SELECT a.literal_value,c.literal_value from kpt b JOIN literal a ON b.literal_id=a.literal_id JOIN literal c ON b.pt__literal_id=c.literal_id"

sqlite3 $db_name "CREATE VIEW kanji_part_concat(kanji,parts_list) AS select kanji , group_concat(part) from kanji_part group by kanji"

sqlite3 $db_name "create view kanji_by_part_meaning as select * from literal natural join kpt join meaning on kpt.pt__literal_id = meaning.literal_id join literal a on a.literal_id=kpt.pt__literal_id where m_lang_id=1"

sqlite3 $db_name "CREATE INDEX idx_kpt_pt__literal_id ON kpt (pt__literal_id);"
sqlite3 $db_name "CREATE INDEX idx_literal_value ON literal (literal_value);"
sqlite3 $db_name "CREATE INDEX idx_meaning_value ON meaning (meaning_value);"
echo Done

