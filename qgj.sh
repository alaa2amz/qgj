iconv  -f EUC-JP -t UTF-8 ../sources/kradfile2 > u_kradfile2
iconv  -f EUC-JP -t UTF-8 ../sources/kradfile > u_kradfile
grep -o -e '^[^#]' u_kradfile u_kradfile2 > krad_1_2_chars_only.txt
grep -o -e '^[^#]' kradfile-u > kradfile_u_only_char.txt
grep -oh -e '^[^#]' u_kradfile u_kradfile2 > krad_1_2_chars_only.txt
comm -3 sorted_kradfile_12.txt  sorted_kradfile_u.txt > krad-u-unique.txt
awk '{print "^"$1}' krad-u-unique.txt > kru-only.txt 

