from xml.etree import ElementTree as ET
import os

items = 'Boeing 737, Boeing 777, Boeing 747, Boeing 787, Airbus A320, Airbus A321, Airbus A220, Airbus A330, \
        Airbus A350, COMAC C919, COMAC ARJ21, other-airplane, passenger ship, motorboat, fishing boat, \
        tugboat, engineering ship, liquid cargo ship, dry cargo ship, warship, other-ship, small car, bus, cargo truck, \
        dump truck, van, trailer, tractor, truck tractor, excavator, other-vehicle, baseball field, basketball court, \
        football field, tennis court, roundabout, intersection, bridge'
items = [item.strip() for item in items.split(',')]
convert_options = {}

for item in items:
    if 'Boeing' in item or 'Airbus' in item or 'COMAC' in item or item == 'other-airplane':
        if 'Airbus' in item:
            convert_options[item.replace('Airbus ', '').lower()] = 'plane'
        elif 'COMAC' in item:
            convert_options[item.replace('COMAC ', '').lower()] = 'plane'
        else:
            convert_options[item] = 'plane'
            convert_options[item.lower()] = 'plane'
            convert_options[item.lower().replace(' ','')] = 'plane'
    elif item in ['small car', 'bus', 'cargo truck', 'dump truck', 'van', 'trailer', 'tractor', 'truck tractor', 'other-vehicle', 'excavator']:
        convert_options[item] = 'vehicle'
    else:
        print ("Skipping ", item)
        convert_options[item] = 'ignore'

def convert_XML_to_DOTA(filename):
    mydoc = ET.parse(filename)
    root = mydoc.getroot()

    objects = root.find('objects')
    items = objects.findall('object')
    output_file = os.path.splitext(os.path.split(filename)[-1])[0] + '.txt'
    with open(f'labelTxt/FAIR1M_{output_file}', 'w') as f:
        ann_list = []
        for item in items:
            label = item.find('possibleresult')
            points = item.find('points')
            label=label.find('name').text
            mapped_label = convert_options[label] if label in convert_options.keys() else convert_options[label.lower()]
            if mapped_label != 'ignore':
                points = [[int(float(item)) for item in point.text.split(',')] for point in points.findall('point')]
                x1, y1 = points[0]
                x2, y2 = points[1]
                x3, y3 = points[2]
                x4, y4 = points[3]
                ann = [x1, y1, x2, y2, x3, y3, x4, y4, mapped_label, 1]
                ann = [str(item) for item in ann]
                ann_list.append(' '.join(ann))
                print (label, mapped_label, x1, y1, x2, y2, x3, y3, x4, y4)

        f.write('\n'.join(ann_list))

if __name__ ==  '__main__':
    xml_files = os.listdir('labelXmls')
    os.makedirs('labelTxt', exist_ok=True)
    for file in xml_files:
        convert_XML_to_DOTA(os.path.join('labelXmls', file))

