import numpy as np
import cv2 
import os
from shutil import copyfile

# Objective
# 1 image has 1 txt in this
# ['x 1', 'y 1', 'x 2', 'y 2', 'x 3', 'y 3', 'x 4', 'y 4', 'category', 'difficult'])

def check_annotations(file_name, img_dir, ann_dir, show=True, outputdir=None):
    colored_img = file_name + '_co.png'
    ir_img = file_name + '_ir.png'
    ann_file = ann_dir + file_name + '.txt'
    
    print ("Processing: ", filename)

    class_dict = {
        1: 'car',
        2: 'truck',
        11: 'pickup',
        4: 'tractor',
        5: 'camping car',
        6: 'boat',
        7: 'motorcycle',
        8: 'bus',
        9: 'van',
        10: 'other',
        11: 'car',
        12: 'large',
        31: 'plane',
        23: 'boat'
    }
    
    filter_options = ['car', 'truck', 'van', 'plane']
    convert_options = {'car': 'small-vehicle', 'truck': 'large-vehicle', 'van': 'large-vehicle', 'plane': 'plane'}
    
    ann_list = []
    has_filtered_items = False
    with open(ann_file, 'r') as ann:
        lines = ann.readlines()
        for line in lines:
            arr = [int(float(item)) for item in line.split(' ')]
            try:
                x_center, y_center, angle, class_index, entirely_contained, occluded, x1, x2, x3, x4,y1, y2, y3, y4 = arr
            except ValueError:
                print ("{} has NOT ENOUGH VALUES.".format(filename))
                return
            class_name = class_dict[class_index]
            if class_name in filter_options:
                # hardcode difficulty
                ann = [x1, y1, x2, y2, x3, y3, x4, y4, convert_options[class_name], 1]
                ann = [str(item) for item in ann]
                ann_list.append(' '.join(ann))
                has_filtered_items = True
    
    if not has_filtered_items:
        print ("Does not have filtered items for : ", filename)
        return 
    
    label_dir = os.path.join(output_dir, 'orig_labelTxt/')
    os.makedirs(label_dir, exist_ok=True)
    with open(label_dir + 'vedai_' + colored_img.replace('.png', '.txt'), 'w') as f:
        f.write('imagesource: VEDAI\n')
        f.write('gsd: -1\n')
        f.write('\n'.join(ann_list))
    
    with open(label_dir + 'vedai_' + ir_img.replace('.png', '.txt'), 'w') as f:
        f.write('imagesource: VEDAI\n')
        f.write('gsd: -1\n')
        f.write('\n'.join(ann_list))
        
    # output_images_dir = os.path.join(output_dir, 'images/')
    # os.makedirs(output_images_dir, exist_ok=True)
    # copyfile(img_dir + colored_img, output_images_dir + 'vedai_' + colored_img)
    # copyfile(img_dir + ir_img, output_images_dir + 'vedai_' + ir_img)
    
    return
        
if __name__ == '__main__':
    img_dir = 'Vehicules1024/'
    ann_dir = 'Annotations1024/'
    output_dir = 'VEDAI_DOTA/'
    filenames = os.listdir(ann_dir)
    for filename in filenames:
        if '.txt' in filename:
            if 'fold' in filename or 'annotation1024' in filename:
                continue
            filename = filename.replace('.txt', '')
            check_annotations(file_name=filename, img_dir=img_dir, ann_dir=ann_dir, show=False, outputdir=output_dir)