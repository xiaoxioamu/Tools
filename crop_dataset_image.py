import cv2 
import os 
import time
import numpy
import shutil
from copy import deepcopy
from rich.progress import track
from draw_boxes import xyxy2xywh, xywhToxyxy


class ImageProc:

	"""
	Crop image to needed size.

	Args:
		label_table (str): Label table
		style (str): The label coordinate format
		size (int): Size of cropped image
		img_shape (tuple): Image shape (weight, height)
	"""

	def __init__(self, 
				label_table: str, 
				img_shape: tuple, 
				size: int,
				style: str="xyxy", 
				):

		self.style = style
		self.shape = img_shape
		self.size = size 
		with open(label_table) as f:
			self.label_path_list = f.readlines()
		
	
	def label2xywh(self, label_path) -> list :

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
					if self.style == "xyxy":
						box = xyxy2xywh(box)

					box.insert(0, class_name)
					boxes_coor.append(box)
			return boxes_coor 


	def label2xyxy(self, label_path: str) -> list :

		"""
		Convert label txt annotations' coordinate to xywh and output image bounding box coordinates.

		Args:
			label_path (str): Label path
		
		Return:
			list [['classname', xmin, ymin, xmax, ymax],]
		"""
 
		boxes_coor = []
		if os.path.exists(label_path):
			with open(label_path) as f:
				boxes = f.readlines()
				for box in boxes:
					box = box.strip().split(' ')
					class_name = box.pop(0)
					box = [float(i) for i in box]
					if self.style == "xywh":
						box = xywhToxyxy(box)

					box.insert(0, class_name)
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
							box_coor = [int(i) for i in box_coor[1:]]
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
							box_coor = [int(i) for i in box_coor[1:]]

							xmin, ymin = (int(i) if i > 0 else 0 for i in (box_coor[0] - size / 2, box_coor[1] - size / 2))	
							temp = box_coor[0] + size / 2, box_coor[1] + size / 2
							xmax, ymax = (int(j) if j <= self.shape[i] else self.shape[i] for i, j in enumerate(temp))
							box_coor_c = [xmin, ymin, xmax, ymax]

							cropped_img = img[box_coor_c[1]:box_coor_c[3], box_coor_c[0]:box_coor_c[2]]
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
							box_coor = [int(i) for i in box_coor[1:]]
							start_point, end_point = (box_coor[0], box_coor[1]), (box_coor[2], box_coor[3])
							boxed_image = cv2.rectangle(img, start_point, end_point, color=(0, 0, 255), thickness=2)	
							cv2.imwrite("test.jpg", boxed_image)	

				except cv2.error:
					print(f"✈️✈️✈️✈️ cv2.error ✈️✈️✈️✈️	\nlabel_path: {label_path}\nimage_path: {img_path}\n")


	def label_save(self, label_path: str, value: int) -> str:

		"""
		Save image to specified path.
		Args:
			label_path (str): Input image path
			value (int): The size of image to crop
		"""

		label_path_list = label_path.split('/')

		crop_eq_value = f"cropped_" + str(value) 
		label_new_dirs = os.path.join(label_path_list[0], crop_eq_value, label_path_list[1]) 
		label_new_path = os.path.join(label_new_dirs, label_path_list[-1])
		label_new_path_list = label_new_dirs.split('/')

		temp_dir = ""
		for i in label_new_path_list:
			temp_dir += i
			if not os.path.exists(temp_dir):
				os.mkdir(temp_dir)
			temp_dir += '/'

		if not os.path.exists(label_new_path):
			shutil.copyfile(label_path, label_new_path)		


	def image_save(self, label_path: str, value: int, img: numpy.ndarray) -> str:

		"""
		Save image to specified path.
		Args:
			label_path (str): Input image path
			value (int): The size of image to crop
			img (numpy.ndarary): Image after cv2.imread
		"""

		img_path = label_path.replace("labels", "images").replace(".txt", ".jpg")
		img_path_list = img_path.split('/')

		crop_eq_value = f"cropped_" + str(value) 
		img_new_dirs = os.path.join(img_path_list[0], crop_eq_value, img_path_list[1])
		img_new_path = os.path.join(img_new_dirs, img_path_list[-1])
		img_new_dirs_list = img_new_dirs.split('/')

		temp_dir = ""
		for i in img_new_dirs_list:
			temp_dir += i
			if not os.path.exists(temp_dir):
				os.mkdir(temp_dir)
			temp_dir += '/'
		if not os.path.exists(img_new_path):
			cv2.imwrite(img_new_path, img)


	def update_label_engine(self, boxes_coor_xyhw: list, img: numpy.ndarray) -> tuple :

		"""
		Update label engine, calculate label iteratively.

		Args:
			box_coor_xyhw (list): Sorted label list which format is xyhw with normal size.
			img (numpy.ndarray): Original image matrix after cv2.imread.
		"""

		box_base = boxes_coor_xyhw[0]
		xmin, ymin = (int(i) if i > 0 else 0 for i in (box_base[1] - self.size / 2, box_base[2] - self.size / 2))	
		temp = box_base[1] + self.size / 2, box_base[2] + self.size / 2
		xmax, ymax = (int(j) if j <= self.shape[i] else self.shape[i] for i, j in enumerate(temp))
		img_base_xyxy = [box_base[0], xmin, ymin, xmax, ymax]
		img_coor_bias = img_base_xyxy[1], img_base_xyxy[2] 

		# boxes_coor_xyhw_cr = []
		# boxes_coor_xyxy_cr = []

		cropped_img = deepcopy(img[img_base_xyxy[2]:img_base_xyxy[4], img_base_xyxy[1]:img_base_xyxy[3]])
		
		img_label = []
		for box_coor in deepcopy(boxes_coor_xyhw):		

			box_coor[1] -= img_coor_bias[0]
			box_coor[2] -= img_coor_bias[1]
			# boxes_coor_xyhw_cr.append(box_coor)
			box_coor[1:] = xywhToxyxy(box_coor[1:])
			box_coor = [int(i) if not isinstance(i, str) else i for i in box_coor]

			if box_coor[3] > self.size or box_coor[4] > self.size:
				return img_label, cropped_img

			# start_point, end_point = (box_coor[0], box_coor[1]), (box_coor[2], box_coor[3])
			# boxed_image = cv2.rectangle(cropped_img, start_point, end_point, color=(0, 0, 255), thickness=2)
			# cv2.imwrite("test.jpg", boxed_image)
			boxes_coor_xyhw.pop(0)
			img_label.append(box_coor)

			if not boxes_coor_xyhw:
				return img_label, cropped_img
			
			
	def update_label(self):

		"""
		Update cropped image label

		Args:
			size (int): Specify the image size to crop			
		"""

		for label_path, _, img_path in self.get_label_img_path():
			time.sleep(0.5)
			if os.path.exists(label_path) and os.path.exists(img_path):
				try:
					img = cv2.imread(img_path)
					boxes_coor = self.label2xywh(label_path)
					boxes_coor_xyhw = []
					if boxes_coor is not None: 
						for box_coor in boxes_coor:
							box_coor = [int(i) if not isinstance(i, str) else i for i in box_coor]
							boxes_coor_xyhw.append(box_coor)
						boxes_coor_xyhw.sort(key=lambda x : x[1])

					boxes_coor_xyhw_dc = deepcopy(boxes_coor_xyhw)
					while boxes_coor_xyhw_dc:
						img_labels, cropped_img = self.update_label_engine(boxes_coor_xyhw_dc, img)

						# for img_label in img_labels:
						# 	start_point, end_point = (img_label[1], img_label[2]), (img_label[3], img_label[4])
						# 	boxed_image = cv2.rectangle(cropped_img, start_point, end_point, color=(0, 0, 255), thickness=2)
						# 	cv2.imwrite("test.jpg", boxed_image)	

				except cv2.error:
					print(f"✈️✈️✈️✈️ cv2.error ✈️✈️✈️✈️	\nlabel_path: {label_path}\nimage_path: {img_path}\n")


	# For test
	def detect_img_objects(self) -> None:

		"""
		Cropped image's object and save to specified directory.
		"""

		for label_path, _, img_path in self.get_label_img_path():
			time.sleep(0.5)
			if os.path.exists(label_path) and os.path.exists(img_path):
				try:
					img = cv2.imread(img_path)
					boxes_coor = self.label2xyxy(label_path)
					if boxes_coor is not None:
						for box_coor in boxes_coor:
							box_coor = [int(i) for i in box_coor[1:]]
							# cropped_img = img[box_coor[1]:box_coor[3], box_coor[0]:box_coor[2]]
							start_point, end_point = (box_coor[0], box_coor[1]), (box_coor[2], box_coor[3])
							boxed_image = cv2.rectangle(img, start_point, end_point, color=(0, 0, 255), thickness=2)
							cv2.imwrite("test.jpg", boxed_image)
				
				except cv2.error:
					print(f"✈️✈️✈️✈️ cv2.error ✈️✈️✈️✈️	\nlabel_path: {label_path}\nimage_path: {img_path}\n")


	def detect_spec_size_img(self, size: int) -> None:

		"""
		Crop image's object and save to specified directory.
		
		Args:
			size (int): Specify the image size to crop
		"""

		for label_path, _, img_path in self.get_label_img_path():
			time.sleep(0.2)
			if os.path.exists(label_path) and os.path.exists(img_path):
				try:
					img = cv2.imread(img_path)
					boxes_coor = self.label2xywh(label_path[1:])
					if boxes_coor is not None: 
						for box_coor in boxes_coor:
							time.sleep(0.2)
							box_coor = [int(i) for i in box_coor]

							xmin, ymin = (int(i) if i > 0 else 0 for i in (box_coor[0] - size / 2, box_coor[1] - size / 2))	
							temp = box_coor[0] + size / 2, box_coor[1] + size / 2
							xmax, ymax = (int(j) if j <= self.shape[i] else self.shape[i] for i, j in enumerate(temp))
							box_coor_c = [xmin, ymin, xmax, ymax]

							start_point, end_point = (box_coor_c[0], box_coor_c[1]), (box_coor_c[2], box_coor_c[3])
							boxed_image = cv2.rectangle(img, start_point, end_point, color=(0, 0, 255), thickness=2)

							cv2.imwrite("test.jpg", boxed_image)

				
				except cv2.error:
					print(f"✈️✈️✈️✈️ cv2.error ✈️✈️✈️✈️	\nlabel_path: {label_path}\nimage_path: {img_path}\n")


if __name__ == "__main__":
	label_tables_list = ["labels/test.txt", "labels/train.txt", "labels/other.txt"]
	crop_size = 640
	image_shape = (2048, 2048)
	
	for label_table in label_tables_list:
		image_proc = ImageProc(label_table, image_shape, crop_size)
		# image_proc.crop_img_objects()
		# image_proc.crop_spec_size_img(crop_size)
		# image_proc.detect_img_objects()
		image_proc.update_label()