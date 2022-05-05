import cv2 
import os 
from rich.progress import track
from draw_boxes import xyxy2xywh, xywh2xyxy


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
					box = [float(i) for i in box.pop(0)]
					if self.style == "xywh":
						box = xywh2xyxy(box)

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

			img = cv2.imread(img_path)
			boxes_coor = self.label2xyxy(label_path)

			for box_coor in boxes_coor:
				box_coor = [int(i) for i in box_coor]
				cropped_img = img[box_coor[0]:box_coor[2], box_coor[1]:box_coor[3]]
				cv2.imshow("cropped", cropped_img)
				cv2.waitKey(0)



if __name__ == "__main__":
	label_tables_list = ["labels/test.txt"]
	
	for label_table in label_tables_list:
		image_crop = ImageCrop(label_table)
		image_crop.crop_image()