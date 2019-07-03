mkdir sources
cd $_
while read x
do
    wget $x
    done < ../urls.txt
