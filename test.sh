#!/bin/bash
git add test.sh 

is_change=0
temFile="temFile"
git status > $temFile
while read line
do
# echo $line
 	if line="Changes to be committed:"
	then
		is_change=1
	fi

done < temFile

a=10
b=10
if [ $a == $b ]
then 
	git commit -m "automatically update"
	git push
fi
