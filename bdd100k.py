import os
import re
import json
import shutil
from rich.progress import track


def read_bbd100(path, label_save_dir, image_save_dir):
    with open(path) as f:
        datas = json.load(f)
    timeofdays = []

    for data in track(datas):
        name, attributes, labels = data['name'], data['attributes'], data['labels']
        timeofday = attributes['timeofday']
        bbox_lists = []
        for label in labels:
            category = label['category']
            bbox_list = [0, 0, 0, 0, 0]
            if 'box2d' in label and timeofday == 'night' and category == 'traffic sign':
                box2d = label['box2d']
                bbox_list[:] = label['category'], box2d['x1'], box2d['y1'], box2d['x2'], box2d['y2']
                bbox_lists.append(bbox_list)

        label_path = label_save_dir + name.replace("jpg", "txt")
        img_path = image_save_dir + name
        source_img_path = "train/" + name

        if bbox_lists and os.path.exists(source_img_path):
            shutil.copyfile(source_img_path, img_path)
            with open(label_path, 'w') as f:
                for bbox in bbox_lists:
                    bbox = re.sub('[\[|\]|\']', '', str(bbox)) + '\n'
                    f.write(bbox)

    return timeofdays


def str_add(path):
    with open(path) as f:
        lines = f.readlines()
    with open(path, 'w') as f:
        for line in lines:
            line = 'train/' + line
            f.write(line)


if __name__ == "__main__":
    path = "bdd100k_labels_images_train.json"
    night_file = "night_file.txt"
    label_save_dir = "night_bdd_label/"
    image_save_dir = "night_bdd_image/"
    timeofdays = read_bbd100(path, night_file, label_save_dir, image_save_dir)
    # print(timeofdays)
    # str_add(night_file)
