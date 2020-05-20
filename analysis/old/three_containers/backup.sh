tmpfile=$(mktemp -d results/result.XXXXXX)

cp *.png $tmpfile/
cp *.plt $tmpfile/
cp *.dat $tmpfile/
cp *.py $tmpfile/
cp *.txt $tmpfile/
cp ../../systemtap/stap_result $tmpfile/
