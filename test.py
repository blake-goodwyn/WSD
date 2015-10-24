__author__ = 'Richard Goodwyn'
import time
import buildDict
import dataReader, contextHandler, main
import numpy as np
import gc

def train():

    ###main testing script
    print 'Building Dictionary...'
    Dict = buildDict.main()
    assert ((type(Dict) == dict) and (Dict != {}))
    print "Dictionary built."

    data = dataReader.train_read()
    #data = dataReader.test_read()

    count = 1
    correct_score = 0
    breakpoint = 100

    ##random sampling parameters
    rand_array = np.random.randint(0, len(data.keys())-1, size=breakpoint)
    train_keys = data.keys()
    test_array = []
    for i in rand_array:
        test_array.append(train_keys[i])

    start = time.time()
    for test_inst in test_array: #data.keys():
        #gc.enable()
        print "Element " + str(count)
        count += 1

        contextElem = data[test_inst]['context']
        target = data[test_inst]['target']
        if type(target) != None:
            bestID = main.processElem(contextElem, target, Dict)

            print str(test_inst) + ", " + str(bestID)

            #print "\n" + str(target)
            #print metricTracker
            #print "\nGuess : " + str(bestID)
            #print "Answer : " + str(train_data[test_inst]['answer'])
            if bestID == data[test_inst]['answer']:
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

def test():

    Dict = buildDict.main()

    data = dataReader.test_read()

    start = time.time()
    for test_inst in data.keys():
        gc.enable()
        contextElem = data[test_inst]['context']
        target = data[test_inst]['target']
        if type(target) != None:
            bestID = main.processElem(contextElem, target, Dict)

            print str(test_inst) + ", " + str(bestID)

    end = time.time()

    print "\n Time : " + str((end-start))

test()