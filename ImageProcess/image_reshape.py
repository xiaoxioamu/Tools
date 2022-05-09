import re
import cv2 
import imgaug.augmenters as iaa
import imgaug as ia
from .crop_dataset_image import ImageProc


class ResizeImage(ImageProc):
	
	def extract_image(self):
		"""
		Extract image shape less than value.
		"""
		pass 


	def resize(self):
		for label_path, _, img_path in self._get_label_img_path():
			seq = iaa.Resize(self.size)
			img = cv2.imread(img_path)
			boxes_coor = self._label2xyxy(label_path)
			boxes_coor_aug = []

			if img.shape[0] < self.size or img.shape[1] < self.size:
				seq_det = seq.to_deterministic()
				for i in boxes_coor:
					box_coor = ia.BoundingBoxesOnImage([
						ia.BoundingBox(x1=i[1], y1=i[2], x2=i[3], 
						y2=i[4], label=i[0])], shape=img.shape)					
					box_coor_aug = seq_det.augment_bounding_boxes(box_coor)[0]
					img_aug = seq_det.augment_image(img)

					label = re.findall('\w*', box_coor_aug.label)[0]
					xmin = box_coor_aug.x1
					ymin = box_coor_aug.y1 
					xmax = box_coor_aug.x2 
					ymax = box_coor_aug.y2				
					boxes_coor_aug.append([label, xmin, ymin, xmax, ymax])
					boxes_coor_aug

				img_new_path, label_new_path = self._image_label_new_path(label_path)
				self._label_save(label_new_path, boxes_coor_aug)	
				self._image_save(img_new_path, img_aug)	


def run():
	label_tables = ["labels/cropped_640/train.txt", 
					"labels/cropped_640/test.txt", 
					"labels/cropped_640/other.txt"]
	img_shape = (2048, 2048)
	cropped_size = 640
	sleep_time = 0
	style = "xyxy"
	proc_name = "resize"

	for label_table in label_tables:
		resize = ResizeImage(
			label_table, 
			img_shape, 
			cropped_size, 
			sleep_time, 
			proc_name,
			style,
		)

		resize.resize()


if __name__ == "__main__":
	run()
			

