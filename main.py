from WSD import buildDict, dataReader, wordGloss, contextHandler

__author__ = 'Richard Goodwyn'
from nltk.corpus import wordnet as wn
import time

def process(element, target):

    [preTarget, postTarget] = contextHandler.contextParser(element)


    target = wn.morphy(target)
    if target.endswith('ing'):
        target = target[:-3]

    #formation of targetGlossArray
    targetGlossArray = {}
    for i in Dict.keys():  #word
        if target in i:
            for j in Dict[i]['sense']:  #senseID
                targetGlossArray[j['-id']] = j
    if targetGlossArray == {}:
        print "Target word (" + str(target) + ") not found in dictionary"


    ##counter object for tracking metric relative to each senseID
    metricTracker = {}
    for i in targetGlossArray.keys():
        metricTracker[i] = 0

    ##pre-context
    metricTracker = contextHandler.compIterator(preTarget,targetGlossArray,metricTracker,1.25)

    ##post-context
    metricTracker = contextHandler.compIterator(postTarget,targetGlossArray,metricTracker,1.25)  #hard-coded rampdown value

    ##score tabulation
    bestID = ""
    score = 0
    for i in metricTracker.keys():
        if metricTracker[i] > score:
            bestID = i
            score = metricTracker[i]

    return bestID, metricTracker

###main testing script
print 'Building Dictionary...'
Dict = buildDict.main()
assert ((type(Dict) == dict) and (Dict != {}))
print "Dictionary built."

train_data = dataReader.train_read()

count = 1
correct_score = 0
breakpoint = 50
start = time.time()

##random sampling parameters
#rand_array = np.random.randint(0, len(train_data.keys())-1, size=breakpoint)
#train_keys = train_data.keys()
#test_array = []
#for i in rand_array:
#    test_array.append(train_keys[i])

for test_inst in train_data.keys():
    print "Element " + str(count)
    count += 1

    contextElem = train_data[test_inst]['context']
    target = train_data[test_inst]['target']
    [bestID, metricTracker] = process(contextElem,target)

    #print "\n" + str(target)
    #print metricTracker
    #print "\nGuess : " + str(bestID)
    #print "Answer : " + str(train_data[test_inst]['answer'])
    if bestID == train_data[test_inst]['answer']:
        print "Correct!"
        correct_score += 1.0
    else:
        print "Incorrect"

    if count == breakpoint+1:
        break

end = time.time()

print "Number of test instances : " + str(breakpoint)
print "Average Score : " + str(correct_score/(breakpoint)*100)
print "Total time : " + str((end - start))
print "Time / element : " + str((end - start)/(breakpoint))