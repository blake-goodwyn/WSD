__author__ = 'LaurenceRosenzweig'

# import xml.etree.ElementTree as ET
#
# def getRoot():
#     tree = ET.parse('Dictionary.xml')
#     root = tree.getroot()
#     print 'root'
#     print root

import json as simplejson
import yaml

def getRoot():
    obj = yaml.safe_load(open('Dictionary.json').read())
    print(repr(obj))