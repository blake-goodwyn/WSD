__author__ = 'Richard Goodwyn'
from nltk.corpus import wordnet as wn
import nltk
import time
import buildDict, dataReader, contextHandler
import gc
import sys

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

    #gc.enable()  # asserts clean up of unnecessary variables by end of processing
    t1 = time.time()
    [preTarget, postTarget] = contextHandler.contextParser(element)
    t2 = time.time()
    #print "Handling : " + str((t2-t1))

    #target word pre-processing
    if type(target) == None or target == "":
        target = ""
    else:
        target = wn.morphy(target)
        if target.endswith('ing'):
            target = target[:-3]
        elif target.endswith('s'):
            target = target[:-1]

    #formation of targetGlossArray
    targetGlossArray = {}
    for i in Dict.keys():  #word
        if target in i:
            for j in Dict[i]['sense']:  #senseID
                targetGlossArray[j['-id']] = j
                targetGlossArray[j['-id']]['-gloss'] = contextHandler.wordFilter(nltk.word_tokenize(str(targetGlossArray[j['-id']]['-gloss'])) + nltk.word_tokenize(str(targetGlossArray[j['-id']]['-synset'])),add=False)


    ##counter object for tracking metric relative to each senseID
    metricTracker = {}
    for i in targetGlossArray.keys():
        metricTracker[i] = 0

    stopwords = nltk.corpus.stopwords.words('English')
    additionalStopWords = ['(',')',',','.',':','"','?','!','*','(',')']
    stopwords.extend(additionalStopWords) #make stop words list more robust

    t3 = time.time()
    ##pre-context
    metricTracker = contextHandler.compIterator(preTarget, targetGlossArray, metricTracker, stopwords, 1.15)

    ##post-context
    metricTracker = contextHandler.compIterator(postTarget, targetGlossArray, metricTracker, stopwords, 1.15)  #hard-coded rampdown value
    t4 = time.time()

    #print "Scoring : " + str((t4-t3))

    ##score tabulation
    bestID = ""
    score = 0
    for i in metricTracker.keys():
        if metricTracker[i] > score:
            bestID = i
            score = metricTracker[i]

    return bestID
