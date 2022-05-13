import os 
import re 
from rich.progress import track 

def get_label_img_path(label_list) -> tuple :

	"""
	From label table iterat input label and image path.
	"""

	for label_path in track(label_list):
		label_path = label_path.strip() 
		img_dir = os.path.split(label_path)[0].replace('labels', 'images')
		img_path = os.path.join(img_dir, os.path.split(label_path)[1].replace('.txt', '.jpg')) 

		yield label_path, img_dir, img_path


def image_label_new_path(label_path: str, prefix) -> tuple :

	"""
	According to label path, get new image and label path.

	Args:
		label_path (str): Label path
	"""

	img_path = label_path.replace("labels", "images").replace(".txt", ".jpg")
	new_dir = f"{prefix}" + '/'
	index = re.search('/', img_path).span()[1]

	img_new_path = img_path[:index] + new_dir + img_path[index:]
	label_new_path = label_path[:index] + new_dir + label_path[index:]

	return img_new_path, label_new_path


def get_bbox_value(label_path: str) -> list :

	"""
	Convert label txt annotations' coordinate to xywh and output image bounding box coordinates.

	Args:
		label_path (str): Label path
	"""

	boxes_coor = []
	if os.path.exists(label_path):
		with open(label_path) as f:
			boxes = f.readlines()
			for box in boxes:
				box = box.strip().split(' ')
				class_name = box.pop(0)
				box = [float(i) for i in box]
				box.insert(0, class_name)
				boxes_coor.append(box)

	return boxes_coor 


def label_save(label_path: str, img_labels: list):

	"""
	Save image to specified path.
	Args:
		label_path (str): Input image path
		img_label (list): Image label annotations [[xmin, ymin, xmax, ymax]]
	"""
	label_dir = os.path.split(label_path)[0]
	label_dir_list = label_dir.split('/')

	temp_dir = ""
	for i in label_dir_list:
		temp_dir += i
		if not os.path.exists(temp_dir):
			os.mkdir(temp_dir)
		temp_dir += '/'

	if not os.path.exists(label_path):
		with open(label_path, 'w') as f:	
			for label in img_labels:
				# label = str(label).replace('[', '').replace(']', '').replace(', ', ' ') + '\n'
				label = re.sub("[\[|\]|,|']",'', str(label)) + '\n'
				f.write(label)