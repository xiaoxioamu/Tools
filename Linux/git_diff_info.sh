#! /usr/bin/bash

cd ~/Engineer/MyCodes
tree -d -L 1 -i > tempfile 
sed -i '1d' tempfile
sed -i '$d' tempfile

while read line; do 
	if [ ${line} ]; then
		cd ${line}
		if [ -e .git ]; then 
			echo "show  -- 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀 --> "${line}" git log"
			git $1
			echo -e "\n"
		fi; cd ..		
	fi
done < tempfile
rm tempfile