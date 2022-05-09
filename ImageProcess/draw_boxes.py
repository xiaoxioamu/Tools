import os
from rich.progress import track
import cv2

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
		box (list): the object coorindate object center point (x, y) and width, height
	"""

	xmin = (box[0] - 1 / 2 * box[2])
	ymin = (box[1] - 1 / 2 * box[3])
	xmax = (box[0] + 1 / 2 * box[2])
	ymax = (box[1] + 1 / 2 * box[3])
	return [xmin, ymin, xmax, ymax]


def xywh2xyxy(box: list, width: int, height: int) -> tuple:
	"""
	From Normalized xywh (0, 1) label style converts to normal size xyxy style 

	Args:
		box (list): Object's center point's x coordinate, y coordinate, width, height
		width (int): Image's width
		height (int): Image's height 
	"""

	xmin = (float(box[1]) - 1 / 2 * float(box[3])) * width
	xmax = (float(box[1]) + 1 / 2 * float(box[3])) * width
	ymin = (float(box[2]) - 1 / 2 * float(box[4])) * height
	ymax = (float(box[2]) + 1 / 2 * float(box[4])) * height	

	return xmin, ymin, xmax, ymax 


def draw_boxes(path: str, 
				width: int, 
				height: int, 
				style: str, 
				export_dir: str,
				) -> None :
	"""
	Args: 
		path (str): Label table
		width (int): Image's width
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
		img = cv2.imread(img_path)
		if os.path.exists(txt):
			with open(txt) as f:
				boxes = f.readlines()
				for box in boxes:
					box = box.strip().split(' ')
					if style == "xyxy":
						start_point, end_point = tuple([int(float(box[1])), int(float(box[2]))]),\
							tuple([int(float(box[3])), int(float(box[4]))])
					else:
						box = xywh2xyxy(box, width, height)
						start_point, end_point = tuple([int(box[1]), int(box[2])]),\
							tuple([int(box[3]), int(box[4])])
					image = cv2.rectangle(img, start_point, end_point, color=(0, 0, 255), thickness=2)

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
				cv2.imwrite(save_path, image)			


if __name__ == "__main__":
	path_list = ["labels/train.txt", 
						"labels/test.txt", 
						"labels/other.txt"]

	width, height = 2048, 2048
	style = "xyxy"
	export_dir = "boxed_images"
	for path in path_list:
		draw_boxes(path, width, height, style, export_dir)