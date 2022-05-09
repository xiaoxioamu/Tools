import argparse 
from ImageProcess.crop_dataset_image import ImageProc
from ImageProcess.image_reshape import ResizeImage
from ImageProcess.label_to_yolo import FormatConvert, Yolo2Xyxy


def parser_args():

	"""
	Parser main function arguments.
	"""

	parser = argparse.ArgumentParser()
	parser.add_argument('-l', "--label_tables_list", nargs='+', type=str, default=["labels/original/train.txt"], help="label tables list")
	parser.add_argument('-c', "--crop_size", type=int, default=640, help="crop size for image")
	parser.add_argument('-i', "--image_shape", type=tuple, default=(2048, 2048), help="The original size of image")
	parser.add_argument('-t', "--sleep_time", type=float, default=0, help="Sleep time in executation")
	parser.add_argument('-p', "--proc_name", type=str, default='crop', help="Image process name")
	parser.add_argument("--style", type=str, default="xyxy", help="The format of image's label annotations")	
	parser.add_argument('-f', "--function", type=str, default='update_label', help="Called function name")
	args = parser.parse_args()

	return args


def run_crop():
	label_tables_list = ["labels/original/train.txt", 
						"labels/original/test.txt", 
						"labels/original/other.txt"]
	img_shape = (2048, 2048)
	crop_size = 640
	sleep_time = 0
	style = "xyxy"
	proc_name = "crop"

	for label_table in label_tables_list:
		image_proc = ImageProc(label_table, 
								img_shape, 
								crop_size, 
								sleep_time,
								proc_name, 
								style,
								)
		image_proc.update_label()


def run_reshape():

	label_tables_list = ["labels/crop_640/original/train.txt", 
						"labels/crop_640/original/test.txt", 
						"labels/crop_640/original/other.txt"]
	img_shape = (2048, 2048)
	crop_size = 640
	sleep_time = 0
	style = "xyxy"
	proc_name = "resize"

	for label_table in label_tables_list:
		resize = ResizeImage(label_table,
							img_shape, 
							crop_size, 
							sleep_time,
							proc_name, 
							style,
							)
		resize.resize()	


def draw_boxes():
	label_tables_list_ori = ["labels/original/train.txt", 
						"labels/original/test.txt", 
						"labels/original/other.txt"]

	label_tables_list_crop = ["labels/crop_640/original/train.txt", 
						"labels/crop_640/original/test.txt", 
						"labels/crop_640/original/other.txt"]

	label_tables_list_resize = ["labels/resize_640/crop_640/original/train.txt", 
						"labels/resize_640/crop_640/original/test.txt", 
						"labels/resize_640/crop_640/original/other.txt"]
	
	label_tables_list_resize_yolo_xxyy = ["labels/xyxy_640/yolo_640/crop_640/original/train.txt", 
										"labels/xyxy_640/yolo_640/crop_640/original/test.txt", 
										"labels/xyxy_640/yolo_640/crop_640/original/other.txt"]

	img_shape = (2048, 2048)
	crop_size = 640
	sleep_time = 0.3
	style = "xyxy"
	proc_name = "crop"

	for label_table in label_tables_list_resize_yolo_xxyy:
		image_proc = ImageProc(label_table, 
								img_shape, 
								crop_size, 
								sleep_time,
								proc_name, 
								style,
								)
		image_proc.draw_boxes()


def label2yolo():
	label_tables_list = ["labels/crop_640/original/train.txt", 
						"labels/crop_640/original/test.txt", 
						"labels/crop_640/original/other.txt"]
	img_shape = (640, 640)
	proc_name = "yolo"
	style = "xyxy"
	size = 640

	for label_table in label_tables_list:
		format_convert = FormatConvert(label_table, img_shape, proc_name, style, size)
		format_convert.update_label()	


def label2xyxy():
	label_tables = ["labels/yolo_640/crop_640/original/train.txt",
					"labels/yolo_640/crop_640/original/test.txt",
					"labels/yolo_640/crop_640/original/other.txt"]
	img_shape = (640, 640)
	proc_name = "xyxy"
	style = "xywh"
	size = 640

	for label_table in label_tables:
		format_convert = Yolo2Xyxy(label_table, img_shape, proc_name, style, size)
		format_convert.update_label()
if __name__ == "__main__":
	# run_crop()
	# draw_boxes()
	# run_reshape()
	# draw_boxes()
	# label2yolo()
	# label2xyxy()
	draw_boxes()