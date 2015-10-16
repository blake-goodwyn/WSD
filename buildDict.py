__author__ = 'LaurenceRosenzweig'

import xml.etree.ElementTree as ET
tree = ET.parse('Dictionary.xml')
root = tree.getroot()
print 'root'
print root