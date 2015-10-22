__author__ = 'Blake Goodwyn'
import xml.etree.ElementTree as ET
import os
import time

def train_read():
    file  = open('training-data.xml')
    tree = ET.parse(file)
    root = tree.getroot()

    struct = {}
    for child in root:
        #print child.attrib
        for inst in child:
            key = inst.attrib['id']
            struct[key] = {}
            for innards in inst:
                if innards.tag == 'answer':
                    struct[key]['answer'] = innards.attrib['senseid']
                else:
                    struct[key]['context'] = (innards.text + ''.join(map(ET.tostring, innards))).strip()
                    for target in innards:
                        struct[key]['target'] = target.text

    return struct

