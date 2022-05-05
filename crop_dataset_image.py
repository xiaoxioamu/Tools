import cv2 
import os 
from rich.progress import track
from draw_boxes import xyxy2xywh


class ImageCrop:
	"""
	Crop image to needed size.

	Args:
		label_table (str): label table
	"""
	def __init__(self, label_table: str):
		
		with open(label_table) as f:
			self.label_path_list = f.readlines()
		
	
	def label2coor(self, style: str="xyxy") -> list :

		"""
		Convert label txt annotations' coordinate to xywh and output image bounding box coordinates.

		Args:
			style (str): Label's format (xyxy, xywh)
		"""

		for label_path in track(self.label_path_list):
			label_path = label_path.strip() 
			boxes_coor = []
			if os.path.exists(label_path):
				with open(label_path) as f:
					boxes = f.readlines()
					for box in boxes:
						box = box.strip().split(' ')
						if style == "xyxy":
							box = [float(box[i]) for i in box]
							box = xyxy2xywh(box)
						boxes_coor.append(box)
				yield boxes_coor 


	def crop_image(self) -> None:
		for boxes_coor in self.label2coor():
			if 


if __name__ == "__main__":
	label_tables_list = ["label_table_test.txt"]
	
	for label_table in label_tables_list:
		image_crop = ImageCrop(label_table)
		image_crop.crop_image()