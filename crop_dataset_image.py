import cv2 
import os 
from rich.progress import track
from draw_boxes import xyxy2xywh, xywhToxyxy


class ImageCrop:
	"""
	Crop image to needed size.

	Args:
		label_table (str): Label table
		style (str): The label coordinate format
	"""
	def __init__(self, label_table: str, style: str="xyxy"):
		self.style = style
		with open(label_table) as f:
			self.label_path_list = f.readlines()
		
	
	def label2xywh(self) -> list :

		"""
		Convert label txt annotations' coordinate to xywh and output image bounding box coordinates.
		"""

		for label_path in track(self.label_path_list):
			label_path = label_path.strip() 
			boxes_coor = []
			if os.path.exists(label_path):
				with open(label_path) as f:
					boxes = f.readlines()
					for box in boxes:
						box = box.strip().split(' ').pop(0)
						if self.style == "xyxy":
							box = xyxy2xywh(box)
						box = [float(box[i]) for i in box]
						boxes_coor.append(box)
				yield boxes_coor 


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


	def crop_image(self) -> None:

		"""
		Cropped image's object and save to specified directory.
		"""

		for label_path in track(self.label_path_list):
			label_path = label_path.strip() 
			img_dir = os.path.split(label_path)[0].replace('labels', 'images')
			img_path = os.path.join(img_dir, os.path.split(label_path)[1].replace('.txt', '.jpg'))	
			# if os.path.exists(label_path) and os.path.exists(img_path):
			try:
				img = cv2.imread(img_path)
				boxes_coor = self.label2xyxy(label_path)
				if boxes_coor is not None:
					for box_coor in boxes_coor:
						box_coor = [int(i) for i in box_coor]
						# start_point, end_point = (box_coor[0], box_coor[1]), (box_coor[2], box_coor[3])
						cropped_img = img[box_coor[1]:box_coor[3], box_coor[0]:box_coor[2]]

						# image = cv2.rectangle(img, start_point, end_point, color=(0, 0, 255), thickness=2)
						# cv2.imshow("image", cropped_img)
						cv2.imwrite("test.jpg", cropped_img)
			except cv2.error:
				print(f"✈️✈️✈️✈️ cv2.error ✈️✈️✈️✈️	\nlabel_path: {label_path}\nimage_path: {img_path}\n")




if __name__ == "__main__":
	label_tables_list = ["labels/test.txt", "labels/train.txt", "labels/other.txt"]
	
	for label_table in label_tables_list:
		image_crop = ImageCrop(label_table)
		image_crop.crop_image()