__author__ = 'Blake Goodwyn'

import buildDict
import dataReader
import contextHandler
import wordGloss
from nltk.corpus import wordnet as wn
import numpy as np
import nltk
import random
import matplotlib

print 'Building Dictionary...'
Dict = buildDict.main()
assert ((type(Dict) == dict) and (Dict != {}))
print "Dictionary built."

train_data = dataReader.train_read()

phrase_score_array = np.linspace(5.0, 10.0, 2)
word_score_array = np.linspace(.75, 1, 2)
ramp_down_array = np.linspace(1, 1.25, 2)

testTracker = {}
count = 1
max_score = 0
values = []
num_inst = 10
avg_score = 0

for x in phrase_score_array:
    testTracker[x] = {}
    for y in word_score_array:
        testTracker[x][y] = {}
        for z in ramp_down_array:
            testTracker[x][y][z] = 0

            print "Test " + str(count)
            train_score = 0

            train_array_keys = []

            for i in range(0,num_inst):
                t = random.randint(0, len(train_data.keys()))
                train_array_keys.append(train_data.keys()[t])


            for test_inst in train_array_keys:
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
                    phrase_score = x
                    word_score = y
                    ramp_down = z

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

                if bestID in targetGlossArray.keys() and bestID != "":
                    definition = targetGlossArray[bestID]['-gloss']

                if bestID in train_data[test_inst]['answer'] and bestID != "":
                    train_score += 1

                print "\n" + str(target)
                print metricTracker
                print "\nGuess : " + str(bestID)
                print "Answer : " + str(train_data[test_inst]['answer'])
                if bestID == train_data[test_inst]['answer']:
                    print "Correct!"
                else:
                    print "Incorrect"

            train_score = train_score*100/num_inst
            print "\nPhrase Score : " + str(x)
            print "Word Score : " + str(y)
            print "Ramp Down : " + str(z)
            print "Number of test instances : " + str(10)
            print "Training score : " + str(train_score)
            print "\n"
            avg_score = float((avg_score + train_score))/count
            count += 1
            if train_score > max_score:
                max_score = train_score
                values = [x, y, z]


print avg_score
print max_score
print values