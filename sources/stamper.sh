while read part meaning
do
echo 's/\(. :.*\)\('"$part"'\)\(.*\)/\1'"$meaning"'\3/' >> koutput.txt
done < $1

