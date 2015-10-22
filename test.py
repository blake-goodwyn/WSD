from WSD import buildDict, wordGloss, contextHandler

__author__ = 'Richard Goodwyn'
import time
import buildDict

testElem = "Do you know what it is ,  and where I can get one ?  We suspect you had seen the Terrex Autospade ,  which is made by Wolf Tools .  It is quite a hefty spade , with bicycle - type handlebars and a sprung lever at the rear , which you step on to <head>activate</head> it . Used correctly ,  you should n't have to bend your back during general digging ,  although it won't lift out the soil and put in a barrow if you need to move it !  If gardening tends to give you backache ,  remember to take plenty of rest periods during the day ,  and never try to lift more than you can easily cope with . "

print "Begin Context Element Test Analysis."
print "Gathering information..."
start = time.time()
[preTarget,postTarget,target] = contextHandler.contextParser(testElem)
end = time.time()
print "Analysis complete.\n"
print "Context Element Analysis Time:" + str(end - start)

try:
    print "Assertions passed."
except AssertionError:
    print "Assertions Failed."

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
