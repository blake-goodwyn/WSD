from WSD import buildDict, wordGloss, contextHandler

__author__ = 'Richard Goodwyn'
import time
import buildDict

testElem = "My English friend Annie was more or less <head>brought</head> up by her nan in a back - to - back in Manchester ."

print "Begin Context Element Test Analysis."
print "Gathering information..."
start = time.time()
[preTarget,postTarget] = contextHandler.contextParser(testElem)
end = time.time()
print "Analysis complete.\n"
print "Context Element Analysis Time:" + str(end - start)

try:
    print "Assertions passed."
except AssertionError:
    print "Assertions Failed."

print preTarget
print postTarget
target = "brought"

#formation of targetGlossArray
targetGlossArray = {}
for i in defnStruct.keys():  #word
    if target in i:
        for j in defnStruct[i]['sense']:  #senseID
            targetGlossArray[j['-id']] = j


##counter object for tracking metric relative to each senseID
metricTracker = {}
for i in targetGlossArray.keys():
    metricTracker[i] = 0

###target word/context word definitions

##define metric parameters
    phrase_score = 10
    word_score = 1
    ramp_down = 1.05

##pre-context
for i in range(0,len(preTarget)):  #pre-target word phrases
    comp_string = " ".join(list(preTarget[i]))  #reformat to string
    for j in targetGlossArray.keys():  #senseIDs of target word
        if comp_string in targetGlossArray[j]['-gloss']:
            metricTracker[j] += phrase_score*np.power(ramp_down, -i)
        else:
            for word in preTarget[i]:
                glossArray = wordGloss.lookup(word,defnStruct)
                for gloss_word in glossArray:
                    if gloss_word in targetGlossArray[j]['-gloss']:
                        metricTracker[j] += word_score*np.power(ramp_down, -i)

##post-context
for i in range(0,len(postTarget)):
    comp_string = " ".join(list(postTarget[i]))  #reformat to string
    for j in targetGlossArray.keys():  #senseIDs of target word
        if comp_string in targetGlossArray[j]:
            metricTracker[j] += phrase_score*np.power(ramp_down, -i)
        else:
            for word in postTarget[i]:
                if word in targetGlossArray[j]:
                    metricTracker[j] += word_score*np.power(ramp_down, -i)

##score tabulation
bestID = ""
score = 0
for i in metricTracker.keys():
    if metricTracker[i] >= score:
        bestID = i
        score = metricTracker[i]

definition = targetGlossArray[bestID]['-gloss']

print "\n Best Sense Determined."
print "Sense ID : " + bestID
print "\n Definition: " + definition
print score
