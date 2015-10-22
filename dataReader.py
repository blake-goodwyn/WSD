__author__ = 'Blake Goodwyn'
import xml.etree.ElementTree as ET
import os
import time

def read(file):

    tree = ET.parse(open(file))
    root = tree.getroot()

    struct = {}
    for child in root:
        assert child.tag == 'lexelt'
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

def train_read():

    file  = 'training-data.xml'
    struct = read(file)

    return struct

