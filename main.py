__author__ = 'Richard Goodwyn'
from nltk.corpus import wordnet as wn
import time
import buildDict, dataReader, contextHandler

def process(file):

    print 'Building Dictionary...'
    Dict = buildDict.main()
    assert ((type(Dict) == dict) and (Dict != {}))
    print "Dictionary built."

    train_data = dataReader.read(file)
    count = 1
    correct_score = 0

    for test_inst in train_data.keys():
        print "Element " + str(count)
        count += 1

        contextElem = train_data[test_inst]['context']
        target = train_data[test_inst]['target']
        bestID = processElem(contextElem, target, Dict)

        if bestID == train_data[test_inst]['answer']:
            print "Correct!"
            correct_score += 1.0
        else:
            print "Incorrect"

    total_score = 100*(correct_score/len(train_data.keys()))
    print total_score
    return total_score


def processElem(element, target, Dict):

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
