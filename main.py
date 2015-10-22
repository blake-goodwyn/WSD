__author__ = 'Richard Goodwyn'
import buildDict
import dataReader
import contextHandler
import wordGloss
from nltk.corpus import wordnet as wn
import numpy as np
import nltk

print 'Building Dictionary...'
Dict = buildDict.main()
assert ((type(Dict) == dict) and (Dict != {}))
print "Dictionary built."

train_data = dataReader.train_read()

count = 1
correct_score = 0

for test_inst in train_data.keys():
    print "Element " + str(count)
    count += 1
    contextElem = train_data[test_inst]['context']
    [preTarget, postTarget] = contextHandler.contextParser(contextElem)
    target = wn.morphy(train_data[test_inst]['target'])

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

    ###target word/context word definitions

    ##define metric parameters
        phrase_score = 10
        word_score = 1
        ramp_down = 1.25

    ##pre-context
    for i in range(0, len(preTarget)):  #pre-target word phrases
        comp_string = " ".join(list(preTarget[i]))  #reformat to string
        for j in targetGlossArray.keys():  #senseIDs of target word
            dictDef = (targetGlossArray[j]['-gloss'] + " " + targetGlossArray[j]['-synset'])
            if comp_string in dictDef:  #phrase score case
                metricTracker[j] += phrase_score*np.power(ramp_down, -i)
            else:  #regular word case
                for word in preTarget[i]:
                    glossArray = wordGloss.lookup(word) #formation of synset for context word
                    for gloss_def in glossArray:
                        temp = nltk.word_tokenize(gloss_def)
                        for gloss_word in temp:
                            if gloss_word in dictDef:
                                metricTracker[j] += word_score*np.power(ramp_down, -i)

    ##post-context
    for i in range(0, len(postTarget)):  #pre-target word phrases
        comp_string = " ".join(list(postTarget[i]))  #reformat to string
        for j in targetGlossArray.keys():  #senseIDs of target word
            dictDef = dictDef = (targetGlossArray[j]['-gloss'] + " " + targetGlossArray[j]['-synset'])
            if comp_string in dictDef:  #phrase score case
                metricTracker[j] += phrase_score*np.power(ramp_down, -i)
            else:  #regular word case
                for word in postTarget[i]:
                    glossArray = wordGloss.lookup(word) #formation of synset for context word
                    for gloss_def in glossArray:
                        temp = nltk.word_tokenize(gloss_def)
                        for gloss_word in temp:
                            if gloss_word in dictDef:

                                metricTracker[j] += word_score*np.power(ramp_down, -i)

    ##score tabulation
    bestID = ""
    score = 0
    for i in metricTracker.keys():
        if metricTracker[i] > score:
            bestID = i
            score = metricTracker[i]


    if bestID in train_data[test_inst]['answer'] and bestID != "":
        correct_score += 1

    print "\n" + str(target)
    print metricTracker
    print "\nGuess : " + str(bestID)
    print "Answer : " + str(train_data[test_inst]['answer'])
    if bestID == train_data[test_inst]['answer']:
        print "Correct!"
    else:
        print "Incorrect"

print "Number of test instances : " + str(count-1)
print "Average Score : " + str(correct_score/(count-1))