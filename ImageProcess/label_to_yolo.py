import os 
from .draw_boxes import xyxy2nor_xywh, xywh2xyxy
from .crop_dataset_image import ImageProc


class FormatConvert(ImageProc):

	def __init__(self, 
				label_table: str, 
				image_shape: tuple, 
				proc_name: str,
				style: str, 
				size: int, 
				):
		self.shape = image_shape
		self.proc_name = proc_name 
		self.style = style
		self.size = size
		 
		with open(label_table) as f:
			self.label_path_list = f.readlines()


	def _get_bbox_value(self, label_path: str) -> list :

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


	def _label2yolo(self, label_path: str) -> list :

		"""
		Convert label to yolo format.

		Args:
			label_path (str): Label path
		"""

		ori_boxes_coor = self._get_bbox_value(label_path)
		new_boxes_coor = []
		if self.style == "xyxy":
			for box_coor in ori_boxes_coor:
				new_boxes_coor.append(self.xyxy2yolo(box_coor))

		return new_boxes_coor
		

	def update_label(self):
		
		"""
		Update label annotation from xyxy format to yolo format.
		"""

		for label_path, _, _ in self._get_label_img_path():
			if os.path.exists(label_path) :
				boxes_coor = self._label2yolo(label_path)
				_, label_new_path = self._image_label_new_path(label_path)
				self._label_save(label_new_path, boxes_coor) 


class Yolo2Xyxy(FormatConvert):

	def _label2xyxy(self, label_path: str) -> list :

		"""
		Convert label to yolo format.

		Args:
			label_path (str): Label path
		"""

		ori_boxes_coor = self._get_bbox_value(label_path)
		new_boxes_coor = []
		if self.style == "xywh":
			for box_coor in ori_boxes_coor:
				new_boxes_coor.append(self.yolo2xyxy(box_coor))

		return new_boxes_coor
		

	def update_label(self):
		
		"""
		Update label annotation from xyxy format to yolo format.
		"""

		for label_path, _, _ in self._get_label_img_path():
			if os.path.exists(label_path) :
				boxes_coor = self._label2xyxy(label_path)
				_, label_new_path = self._image_label_new_path(label_path)
				self._label_save(label_new_path, boxes_coor) 