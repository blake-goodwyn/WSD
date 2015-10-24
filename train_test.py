from WSD import buildDict, dataReader, wordGloss, contextHandler

__author__ = 'Blake Goodwyn'

import numpy as np
import main
import time

print 'Building Dictionary...'
Dict = buildDict.main()
assert ((type(Dict) == dict) and (Dict != {}))
print "Dictionary built."

train_data = dataReader.train_read()

ramp_down_array = np.linspace(1.15, 1.25, 5)

testTracker = {}
count = 1
breakpoint = 25
##random sampling parameters
rand_array = np.random.randint(0, len(train_data.keys())-1, size=breakpoint)
train_keys = train_data.keys()
test_array = []
for i in rand_array:
    test_array.append(train_keys[i])

for x in ramp_down_array:

    count = 1
    correct_score = 0
    start = time.time()
    for test_inst in test_array:  #data.keys():
        print "Element " + str(count)
        count += 1

        contextElem = train_data[test_inst]['context']
        target = train_data[test_inst]['target']
        if type(target) != None:
            bestID = main.processElem(contextElem, target, Dict, x)

            #print str(test_inst) + ", " + str(bestID)

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
    testTracker[x] = correct_score/(breakpoint)*100
    print "Number of test instances : " + str(breakpoint)
    print "Average Score : " + str(correct_score/(breakpoint)*100)
    print "Total time : " + str((end - start))
    print "Time / element : " + str((end - start)/(breakpoint))


max = 0
best = 0
for i in testTracker.keys():
    if testTracker[i] > max:
        best = i
        max = testTracker[i]

print "Best Value: " + str(i)