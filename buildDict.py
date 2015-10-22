__author__ = 'LaurenceRosenzweig'

import yaml

#Returns JSON dictionary
def getJSON():
    doc = yaml.safe_load(open('Dictionary.json').read())
    return doc

def main():
    temp = getJSON()
    temp = temp['dictionary']['lexelt']
    defnStruct = {}

    for i in temp:
        defnStruct[i['-item']] = i

    return defnStruct