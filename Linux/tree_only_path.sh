#! /usr/bin/bash

# Tree local directory and export to specified file. Delete this file first and last two lines.
# Variable parameter. If output is not specifed, default output name is correct directory's name.

if [ $1 = . ]; then 
	File=$(pwd | grep -o "\w*$").txt
	echo ${File}
else 
	File=$1.txt
fi

if [ $2 ]; then 
	tree -i -f $1 > $2
	sed -i "1d;$(($(wc -l < $2)-1)),\$d" $2
else
	tree -i -f $1 > ${File}
	sed -i "1d;$(($(wc -l < ${File})-1)),\$d" ${File}
fi 
 
