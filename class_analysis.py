# Analysis dataset class information. Find the number of object over specified 
# value and export labels over this value

import os
import shutil
from rich.progress import track
from ImageProcess.utils import *

def class_analysis(label_table):

	with open(label_table) as f:
		labels_path = f.readlines()

	class_names = {}
	for label_path  in labels_path:
		# if os.path.exists(label_path) :
		bboxs = get_bbox_value(label_path.strip())
		for bbox in bboxs:
			class_name = bbox[0]
			if class_name in class_names:
				class_names.update({class_name:class_names[class_name] + 1})
			else:
				class_names.update({class_name:1})				
	return class_names


def class_sum(label_tables):
	class_list = []
	for label_table in label_tables:
		class_names = class_analysis(label_table) 
		class_list.append(class_names)	

	class_all = {}
	for class_names in class_list:
		for class_name in class_names:
			if class_name in class_all:
				class_all.update({class_name:(class_all[class_name] + class_names[class_name])})
			else:
				class_all.update({class_name:class_names[class_name]})
	return class_all


def class_over_100(class_all):
	class_filter = {}
	for class_name in class_all:
		if class_all[class_name] >= 100:
			class_filter.update({class_name:class_all[class_name]})

	return class_filter


def file_over_100(label_tables, proc_name, class_sum):
	for label_table in track(label_tables):
		with open(label_table) as f:
			label_list = f.readlines()
		for label_path in label_list:
			label_path = label_path.strip()
			bboxs = get_bbox_value(label_path.strip()) 
			img_path = re.sub("labels", "images", label_path)
			img_path = re.sub("\.txt", ".jpg", img_path)
			new_bboxs = []
			for bbox in bboxs:
				if bbox[0] in class_sum:
					new_bboxs.append(bbox)
			if new_bboxs:
				img_new_path, label_new_path = image_label_new_path(label_path, proc_name)
				label_save(label_new_path, new_bboxs)
				shutil.copyfile(img_path, img_new_path)


if __name__ == "__main__":
	label_tables = ["Filter_TT100K/train.txt",
					"Filter_TT100K/test.txt"]
	proc_name = 'filter'
	class_all = class_sum(label_tables)
	class_sum = class_over_100(class_all)
	# file_over_100(label_tables, proc_name, class_sum)
	class_sum