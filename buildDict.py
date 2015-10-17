__author__ = 'LaurenceRosenzweig'

import yaml

#Returns JSON dictionary
def getJSON():
    obj = yaml.safe_load(open('Dictionary.json').read())
    return repr(obj)