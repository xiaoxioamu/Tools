import os
import argparse 
import shutil

def calculate_image_size(path: str) -> list : 
	"""
	Calculcate the image's height, weight, area and label's table.

	Args:
		path (str): Label table path
	"""

	with open(path) as f:
		labels_path = f.readlines()

	bboxes_inf = []	
	for label_path in labels_path:
		label_path = label_path.strip()
		if os.path.exists(label_path):
			with open(label_path) as f:
				bboxes = f.readlines()
				for bbox in bboxes:
					bbox = bbox.strip().split(' ')
					bbox = [float(i) for i in bbox[1:]]
					b_w, b_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
					b_inf = b_w, b_h, b_w * b_h, label_path
					bboxes_inf.append(b_inf)
	return bboxes_inf	


def extract_imgs(key: str, file_list: list, value: int) -> None: 

	"""
	Extracted and store the images which cope with the condition value

	Args:
		key (str): over or less, to determine the condition
		file_list (list): the image path needed by extracted
		value (int): the condition value to extract image

	"""

	for file in file_list:
		label_path = file[-1]
		label_path_list = label_path.split('/')
		img_path = label_path.replace("labels", "images").replace(".txt", ".jpg")
		img_path_list = img_path.split('/')

		size_over_value = f"size_{key}_" + str(value) 
		label_new_dirs = os.path.join(label_path_list[0], size_over_value, label_path_list[1]) 
		img_new_dirs = os.path.join(img_path_list[0], size_over_value, img_path_list[1])

		label_new_path = os.path.join(label_new_dirs, label_path_list[-1])
		img_new_path = os.path.join(img_new_dirs, img_path_list[-1])

		for i in (label_new_dirs, img_new_dirs):
			tmp_path = os.path.split(i)
			if not os.path.exists(tmp_path[0]):
				os.makedirs(tmp_path[0])
			if not os.path.exists(i):
				os.makedirs(i)

		if not os.path.exists(label_new_path) or not os.path.exists(img_new_path):
			shutil.copyfile(label_path, label_new_path)
			shutil.copyfile(img_path, img_new_path)


def export_labels_inf(label_inf: tuple, file=None) -> tuple : 

	"""
	Sort label information and export sorted label table.

	Args:
		label_inf (tuple): label information
		file (str): the path where sorted label information will export. 
			If file=None, sorted label information isn't exported.
	"""

	label_inf.sort(key=lambda row: (row[0], row[1]), reverse=True)
	if file:
		with open(file, 'w') as f:
			for i in label_inf:
				f.write(str(i) + '\n')
	return label_inf


def export_labels_comp(key: str, label_inf: list, value: int, file: str=None) -> list :

	"""
	According to the key, to determine which function will be called.
	
	Args:
		key (str): Key word
		label_inf (list): label information
		value (int): threshold
		file (str): the path where sorted label information will export. 
			If file=None, sorted label information isn't exported.

	"""
	if key == "over":
		labels_comp = export_labels_inf_over_num(label_inf, value, file)
	elif key == "less":
		labels_comp = export_labels_inf_less_num(label_inf, value, file)
	return labels_comp 


def export_labels_inf_over_num(label_inf: list, value: int, file: str=None) -> list:

	"""
	Filter the label's weight or height over value. Sorted filtered label information.
		If file is not None, export sorted label information to file.

	Args:
		label_inf (list): building box infomation
		value (int): threshold
		file (str): the path where sorted label information will export. 
			If file=None, sorted label information isn't exported.
	"""

	size_over_value = []
	for i in label_inf:
		if i[0] >= value or i[1] >= value:
			size_over_value.append(i)
	size_over_value.sort(key=lambda row: (row[0]), reverse=True)
	if file:
		with open(file, 'w') as f:
			for i in size_over_value:
				f.write(str(i) + '\n')
	return size_over_value


def export_labels_inf_less_num(label_inf: list, value: int, file: str=None) -> list : 

	"""
	Filter the label's weight or height less value. Sorted filtered label information .
		If file is not None, export sorted label information to file.

	Args:
		label_inf (list): building box infomation
		value (int): threshold
		file (str): the path where sorted label information will export. 
			If file=None, sorted label information isn't exported.
	"""
	
	size_less_value = []
	for i in label_inf:
		if i[0] < value and i[1] < value:
			size_less_value.append(i)
	size_less_value.sort(key=lambda row: (row[0]), reverse=True)
	if file:
		with open(file, 'w') as f:
			for i in size_less_value:
				f.write(str(i) + '\n')
	return size_less_value


def export_label_table(labels_comp: list, labels_table_path: str) -> None :

	"""
	Export label file name to label table file

	Args:
		labels_comp (list): label's information (x, y, w, h)
		labels_table_path (str): label table path
	"""

	with open(labels_table_path, "w") as f:
		for i in labels_comp:
			f.write(str(i[3]) + '\n')


def multi_export(
	path_list: list, 
	label_export_dir: str, 
	hw_value: int, 
	over: bool =True, 
	img_export: bool =False, 
	label_comp_export: bool =False,
				) -> None:	

	"""
	Input label path file list, and export sorted and fitered label information and image
		to specified folds.

	Args:
		path_list (list): label path list
		label_export_dir (str): label information file after filter
		hw_value (int): bounding box weight or height threshold
		over (bool): if over==True, the condition is over the hw_value, 
			if over==False, the condition is less the hw_value
		img_export (bool): if bool==True, export filtered image to specified folder
		label_comp_export (bool): if label_comp_export is True, export label's information 
	"""

	if not os.path.exists(label_export_dir):
		os.makedirs(label_export_dir)
	
	for path in path_list:
		if over:
			key = "over"
		else:
			key = "less"

		bboxes_inf = calculate_image_size(path)
		label_filename = path.split('/')[1].split('.')[0] + "_inf.txt"
		label_comp_filename = path.split('/')[1].split('.')[0] + \
			f"_inf_{key}_" + str(hw_value) + ".txt"
		label_table_filename = path.split('/')[1].split('.')[0] + \
			f"_{key}_" + str(hw_value) + "_table" + ".txt"

		labels_inf_file = os.path.join(label_export_dir, label_filename)
		labels_inf_comp_file = os.path.join(label_export_dir, label_comp_filename)
		labels_table_path = os.path.join(label_export_dir, label_table_filename)

		if label_comp_export:
			export_labels_inf(bboxes_inf, labels_inf_file) 
			labels_comp = export_labels_comp(key, bboxes_inf, hw_value, labels_inf_comp_file)
			export_label_table(labels_comp, labels_table_path)
		if img_export:
			extract_imgs(key, labels_comp, hw_value)	


def parse_args():
	parser = argparse.ArgumentParser(description="Sort image labels, filter images and labels")
	parser.add_argument('-p', "--path_list", type=list, default=["labels/train.txt", "labels/test.txt", "labels/other.txt"], help="label table list")
	parser.add_argument('-l', "--label_export_dir", type=str, default="export", help="Filtered label table exported path")
	parser.add_argument('-v', "--hw_value", type=int, default=300, help="Threshold value to filter")
	parser.add_argument("--over", type=bool, default=True, help="To determine over or less the threshold")
	parser.add_argument("--img_export", type=bool, default=True, help="If img_export is True, image export")
	parser.add_argument("--label_comp_export", type=bool, default=True, help="If label_comp_export is true, sorted label information will be export")
	
	args = parser.parse_args()
	return args


if __name__ == "__main__":
	args = parse_args()
	multi_export(args.path_list, 
				args.label_export_dir, 
				args.hw_value, 
				args.over, 
				args.img_export, 
				args.label_comp_export,
				)