import os
from rich.progress import track
import cv2 as cv

def xyxy2xywh(box: list) -> list :
	"""
	Convert xyxy label style to xywh label style and image size don't normalize to (0, 1)

	Args: 
		box (list): the object coorindate xmin, ymin, xmax, ymax
	"""

	x_c = (box[0] + box[2]) / 2
	y_c = (box[1] + box[3]) / 2
	w = (box[2] - box[0])
	h = (box[3] - box[1])
	return [x_c, y_c, w, h]
	

def xywhToxyxy(box: list) -> list :
	"""
	Convert xyxy label style to xywh label style and image size don't normalize to (0, 1)

	Args: 
		box (list): the object coorindate object center point (x, y) and weight, height
	"""

	xmin = (box[0] - 1 / 2 * box[2])
	ymin = (box[1] - 1 / 2 * box[3])
	xmax = (box[0] + 1 / 2 * box[2])
	ymax = (box[1] + 1 / 2 * box[3])
	return [xmin, ymin, xmax, ymax]


def xywh2xyxy(box: list, weight: int, height: int) -> tuple:
	"""
	From Normalized xywh (0, 1) label style converts to normal size xyxy style 

	Args:
		box (list): Object's center point's x coordinate, y coordinate, weight, height
		weight (int): Image's weight
		height (int): Image's height 
	"""

	xmin = (float(box[1]) - 1 / 2 * float(box[3])) * weight
	xmax = (float(box[1]) + 1 / 2 * float(box[3])) * weight
	ymin = (float(box[2]) - 1 / 2 * float(box[4])) * height
	ymax = (float(box[2]) + 1 / 2 * float(box[4])) * height	

	return xmin, ymin, xmax, ymax 


def draw_boxes(path: str, 
				weight: int, 
				height: int, 
				style: str, 
				export_dir: str,
				) -> None :
	"""
	Args: 
		path (str): Label table
		weight (int): Image's weight
		height (int): Image's height
		style (str): Label's format (xyxy, xywh)
		export_dir (str): The directory of exported image
	"""

	with open(path) as f:
		label_data = f.readlines()
	
	for txt in track(label_data):
		txt = txt.strip()

		img_dir = os.path.split(txt)[0].replace('labels', 'images')
		img_path = os.path.join(img_dir, os.path.split(txt)[1].replace('.txt', '.jpg'))
		img = cv.imread(img_path)
		if os.path.exists(txt):
			with open(txt) as f:
				boxes = f.readlines()
				for box in boxes:
					box = box.strip().split(' ')
					if style == "xyxy":
						start_point, end_point = tuple([int(float(box[1])), int(float(box[2]))]),\
							tuple([int(float(box[3])), int(float(box[4]))])
					else:
						box = xywh2xyxy(box, weight, height)
						start_point, end_point = tuple([int(box[1]), int(box[2])]),\
							tuple([int(box[3]), int(box[4])])
					image = cv.rectangle(img, start_point, end_point, color=(0, 0, 255), thickness=2)

			save_dir = img_dir.replace('images', export_dir).split('/')
			save_dir = os.path.join(save_dir[0], path.split('/')[1][:-10]) 
			save_path = os.path.join(save_dir, os.path.split(img_path)[1])

			save_dir_list = save_dir.split('/')
			temp_dir = ""
			for i in save_dir_list:
				temp_dir += i
				if not os.path.exists(temp_dir):
					os.mkdir(temp_dir)
				temp_dir += '/'
			if not os.path.exists(save_path):
				cv.imwrite(save_path, image)			


if __name__ == "__main__":
	path_list = ["export/other_over_300_table.txt", 
				 "export/test_over_300_table.txt",
				 "export/train_over_300_table.txt"]

	weight, height = 2048, 2048
	style = "xyxy"
	export_dir = "boxed_images"
	for path in path_list:
		draw_boxes(path, weight, height, style, export_dir)