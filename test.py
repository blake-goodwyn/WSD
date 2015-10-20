__author__ = 'Richard Goodwyn'
import contextHandler
import time
import xml.etree.ElementTree as ET
import os
from collections import Counter

testElem = "Do you know what it is ,  and where I can get one ?  We suspect you had seen the Terrex Autospade ,  which is made by Wolf Tools .  It is quite a hefty spade , with bicycle - type handlebars and a sprung lever at the rear , which you step on to <head>activate</head> it . Used correctly ,  you should n't have to bend your back during general digging ,  although it wo n't lift out the soil and put in a barrow if you need to move it !  If gardening tends to give you backache ,  remember to take plenty of rest periods during the day ,  and never try to lift more than you can easily cope with . "

print "Begin Context Element Test Analysis."
print "Gathering information..."
start = time.time()
[preTarget,postTarget,target] = contextHandler.contextParser(testElem)
end = time.time()
print "Analysis complete.\n"
print "Context Element Analysis Time:" + str(end - start)

#print "Pre-context :"
#print preTarget

#print "\nPost-context :"
#print postTarget

#print "\n Target"
#print target

#defining test dictionary structure
defnArray = {}
tree = ET.parse(os.path.join("C:\Users\Blake Goodwyn\Documents\Code\cs4740p2\Atlassian_Repo","testDict.xml"))
root = tree.getroot()
tempStruct = {}
for child in root:
    if child.tag == "sense":
        tempStruct[child.attrib['id']] = child.attrib

defnArray[root.attrib['item']] = tempStruct

#formation of targetGlossArray
targetGlossArray = {}
for i in defnArray.keys(): #word
    if target in i:
        for j in defnArray[i].keys():  #senseID
            targetGlossArray[j] = defnArray[i][j]["gloss"]


##counter object for tracking metric relative to each senseID
metricTracker = {}
for i in targetGlossArray.keys():
    metricTracker[i] = 0

###target word/context word definitions

##pre-context
for i in preTarget:  #pre-target word phrases
    comp_string = " ".join(list(i))  #reformat to string
    for j in targetGlossArray.keys():  #senseIDs of target word
        if comp_string in targetGlossArray[j]:
            metricTracker[j]
        else:
            for word in i:
                i