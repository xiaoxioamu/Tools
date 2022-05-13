# Convert yolo format's annotations [classname, x_c, y_c, w, h] to 
# [classnumber, x_c, y_c, w, h]


from copy import deepcopy
import glob
from os.path import exists
import re


def get_class(dir, class_file):

	filelist = glob.glob(dir + '/**/*.txt', recursive=True)
	class_list = []

	for filename in filelist:
		with open(filename) as f:
			lines = f.readlines()
		if lines:
			for line in lines:
				classname = line.split(' ')[0]

				if classname not in class_list:
					class_list.append(classname)

	with open(class_file, 'w') as f:
		f.write(str(class_list))


def  format2yolov5_items(dir, class_file):

	filelist = glob.glob(dir + '/**/*.txt', recursive=True)
	assert exists(class_file), "File doesn't exist"
	with open(class_file) as f:
		class_list = f.readlines()[0]
	class_list = re.sub("[\[|\]|\s|']", '', class_list).split(',')

	for filename in filelist:
		file = open(filename)
		lines = file.readlines()
		file.close()
		with open(filename, 'w') as f:		
			if lines:
				for line in lines:
					bbox_items = line.strip().split(' ')
					new_bbox_items = deepcopy(bbox_items)
					new_bbox_items[0] = class_list.index(bbox_items[0])
					new_bbox_items = re.sub("[\[|\]|,|']", "", str(new_bbox_items)) + '\n'
					f.write(new_bbox_items)


if __name__ == "__main__":
	dir = "Filter_TT100K"
	class_file = 'class_list.txt'
	get_class(dir, class_file)
	class_index = format2yolov5_items(dir, class_file)