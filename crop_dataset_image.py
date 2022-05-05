import cv2 
import os 
from rich.progress import track
from draw_boxes import xyxy2xywh, xywhToxyxy


class ImageProc:
	"""
	Crop image to needed size.

	Args:
		label_table (str): Label table
		style (str): The label coordinate format
		img_shape (tuple): Image shape (weight, height)
	"""
	def __init__(self, img_shape: tuple, label_table: str, style: str="xyxy"):
		self.style = style
		self.shape = img_shape
		with open(label_table) as f:
			self.label_path_list = f.readlines()
		
	
	def label2xywh(self, label_path) -> list :

		"""
		Convert label txt annotations' coordinate to xywh and output image bounding box coordinates.
		"""

		boxes_coor = []
		if os.path.exists(label_path):
			with open(label_path) as f:
				boxes = f.readlines()
				for box in boxes:
					box = box.strip().split(' ')
					box.pop(0)
					box = [float(i) for i in box]
					if self.style == "xyxy":
						box = xyxy2xywh(box)

					boxes_coor.append(box)
			return boxes_coor 


	def label2xyxy(self, label_path: str) -> list :

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
					box.pop(0)
					box = [float(i) for i in box]
					if self.style == "xywh":
						box = xywhToxyxy(box)

					boxes_coor.append(box)
			return boxes_coor 


	def __len__(self):
		return len(self.label_path_list)


	def get_label_img_path(self) -> tuple :

		"""
		From label table iterat input label and image path.
		"""

		for label_path in track(self.label_path_list):
			label_path = label_path.strip() 
			img_dir = os.path.split(label_path)[0].replace('labels', 'images')
			img_path = os.path.join(img_dir, os.path.split(label_path)[1].replace('.txt', '.jpg')) 

			yield label_path, img_dir, img_path


	def crop_img_objects(self) -> None:

		"""
		Cropped image's object and save to specified directory.
		"""

		for label_path, _, img_path in self.get_label_img_path():
			if os.path.exists(label_path) and os.path.exists(img_path):
				try:
					img = cv2.imread(img_path)
					boxes_coor = self.label2xyxy(label_path)
					if boxes_coor is not None:
						for box_coor in boxes_coor:
							box_coor = [int(i) for i in box_coor]
							cropped_img = img[box_coor[1]:box_coor[3], box_coor[0]:box_coor[2]]
							cv2.imwrite("test.jpg", cropped_img)
				
				except cv2.error:
					print(f"✈️✈️✈️✈️ cv2.error ✈️✈️✈️✈️	\nlabel_path: {label_path}\nimage_path: {img_path}\n")


	def crop_spec_size_img(self, size: int) -> None:

		"""
		Crop image's object and save to specified directory.
		
		Args:
			size (int): Specify the image size to crop
		"""

		for label_path, _, img_path in self.get_label_img_path():
			if os.path.exists(label_path) and os.path.exists(img_path):
				try:
					img = cv2.imread(img_path)
					boxes_coor = self.label2xywh(label_path)
					if boxes_coor is not None: 
						for box_coor in boxes_coor:
							box_coor = [i for i in box_coor]

							xmin, ymin = [int(i) if i > 0 else 0 for i in (box_coor[2] - size / 2, box_coor[3] - size / 2)]	
							xmax, ymax = [int(i) if i <= size else size for i in (box_coor[2] + size / 2, box_coor[3] + size / 2)]	
							box_coor = [xmin, ymin, xmax, ymax]
							cropped_img = img[box_coor[1]:box_coor[3], box_coor[0]:box_coor[2]]
							cv2.imwrite("test.jpg", cropped_img)
				
				except cv2.error:
					print(f"✈️✈️✈️✈️ cv2.error ✈️✈️✈️✈️	\nlabel_path: {label_path}\nimage_path: {img_path}\n")


	def draw_boxes(self) -> None:

		"""
		Cropped image's object and save to specified directory.
		"""

		for label_path, _, img_path in self.get_label_img_path():
			if os.path.exists(label_path) and os.path.exists(img_path):
				try:
					img = cv2.imread(img_path)
					boxes_coor = self.label2xyxy(label_path)
					if boxes_coor is not None:
						for box_coor in boxes_coor:
							box_coor = [int(i) for i in box_coor]
							start_point, end_point = (box_coor[0], box_coor[1]), (box_coor[2], box_coor[3])
							boxed_image = cv2.rectangle(img, start_point, end_point, color=(0, 0, 255), thickness=2)	
							cv2.imwrite("test.jpg", boxed_image)	

				except cv2.error:
					print(f"✈️✈️✈️✈️ cv2.error ✈️✈️✈️✈️	\nlabel_path: {label_path}\nimage_path: {img_path}\n")



if __name__ == "__main__":
	label_tables_list = ["labels/test.txt", "labels/train.txt", "labels/other.txt"]
	crop_size = 640
	
	for label_table in label_tables_list:
		image_proc = ImageProc(label_table)
		# image_proc.crop_img_objects()
		image_proc.crop_spec_size_img(crop_size)