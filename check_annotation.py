import numpy as np
import cv2 
import os

def check_annotations(file_name, img_dir, ann_dir, show=True, outputdir=None):
    colored_img = img_dir + file_name + '_co.png'
    ir_img = img_dir + file_name + '_ir.png'
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
    
    ann_list = []
    colored_img = cv2.imread(colored_img)
    ir_img = cv2.imread(ir_img)
    with open(ann_file, 'r') as ann:
        lines = ann.readlines()
        for line in lines:
            arr = [int(float(item)) for item in line.split(' ')]
            try:
                x_center, y_center, angle, class_index, entirely_contained, occluded, x1, x2, x3, x4,y1, y2, y3, y4 = arr
            except ValueError:
                print ("{} has NOT ENOUGH VALUES.".format(filename))
                return
            colored_img = cv2.circle(colored_img, (x_center,y_center), radius=5, color=(0, 0, 255), thickness=2)
            ir_img = cv2.circle(ir_img, (x_center,y_center), radius=5, color=(0, 0, 255), thickness=2)
            ann_list.append((x1, y1, x2, y2, x3, y3, x4, y4, class_index))


    for item in ann_list:
        x1, y1, x2, y2, x3, y3, x4, y4, class_index = item
        class_name = class_dict[class_index]
        if class_name in ['motorcycle', 'large', 'pickup', 'van']:
            print (class_name, file_name)
        pts = np.array([[x1,y1], [x2,y2], [x3,y3], [x4,y4]], np.int32)
        pts = pts.reshape(-1, 1, 2)
        colored_img = cv2.polylines(colored_img, [pts], True, (0,255,255))
        colored_img = cv2.putText(colored_img, class_name, (x1-5, y1-5), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)
        # ir image 
        ir_img = cv2.polylines(ir_img, [pts], True, (0,255,255))
        ir_img = cv2.putText(ir_img, class_name, (x1-5, y1-5), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)
    
    if show:    
        cv2.imshow("COLORED", colored_img)
        cv2.waitKey(0)
        cv2.imshow("IR", ir_img)
        cv2.waitKey(0)
    else:
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            cv2.imwrite(output_dir + file_name + '_ir.png', ir_img)
            cv2.imwrite(output_dir + file_name + '_co.png', colored_img)
        
if __name__ == '__main__':
    img_dir = 'Vehicules1024/'
    ann_dir = 'Annotations1024/'
    output_dir = 'AnnotatedVehicles/'
    filenames = os.listdir(ann_dir)
    for filename in filenames:
        if '.txt' in filename:
            if 'fold' in filename or 'annotation1024' in filename:
                continue
            filename = filename.replace('.txt', '')
            check_annotations(file_name=filename, img_dir=img_dir, ann_dir=ann_dir, show=False, outputdir=output_dir)