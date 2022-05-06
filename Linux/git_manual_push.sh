#!/bin/bash

<<com
git push to github automatically
com

cd ~/Engineer/MyCodes/Tools
git pull
git add .

is_change=0
temFile=~/Engineer/MyCodes/temp/temFile_push
# comments="automatically update: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"

# Determine if a file is exists, if file is not exists, then creat it.
if [ ! -e ${temFile} ]; then 
	touch ${temFile}
fi 

git status > ${temFile}

# Read temFile's information, if finds changed file, then sets is_change to 1
while read line; do
 	if  test line="Changes to be committed:"; then
		is_change=1
	fi
done < ${temFile}

# Commit and push
if [ $is_change == 1 ]
then 
	git commit -m "$*"
	git push
fi
