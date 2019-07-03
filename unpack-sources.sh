cd sources
for x in *.gz
do
    gzip -kvd "$x"
done

for x in *.zip
do
    unzip "$x"
done
iconv -f EUC-JP -t UTF-8 kradfile > kradfile_utf8

iconv -f EUC-JP -t UTF-8 kradfile2 > kradfile2_utf8
