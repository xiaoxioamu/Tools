#!/bin/bash

<<com
git commit automatically
com

# cd ~/Engineer/MyCodes/Tools
# git add .

cd ~/Engineer/MyCodes
tree -d -L 1 -i > tempfile 
sed -i '1d' tempfile
sed -i '$d' tempfile

while read line; do 
	if [ ${line} ]; then
		cd ${line}
		if [ -e .git ]; then 
			is_change=0
			temFile=~/Engineer/MyCodes/temp/temFile_commit
			# comments="automatically update: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"

			# Determine if a file is exists, if file is not exists, then creat it.
			if [ ! -e ${temFile} ]; then 
				touch ${temFile}
			fi 
			git add .
			git status > ${temFile}

			# Read temFile's information, if finds changed file, then sets is_change to 1
			while read line1; do
				if  test line1="Changes to be committed:"; then
					is_change=1
				fi
			done < ${temFile}

			# Commit and push
			if [ $is_change == 1 ]
			echo "starting commit -- 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀 --> "${line} 
			then 
				git commit -m "automatically update:"📔$(date +"%Y-%m-%d-%H:%M:%S")
			fi
			echo -e "\n"
		fi; cd ..
	fi 
done < tempfile 
