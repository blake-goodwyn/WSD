__author__ = 'Richard Goodwyn'
import time
import buildDict
import dataReader, contextHandler, main
import numpy as np

testElem = "My English friend Annie was more or less <head>brought</head> up by her nan in a back - to - back in Manchester ."

print "Begin Context Element Test Analysis."
print "Gathering information..."
start = time.time()
[preTarget, postTarget] = contextHandler.contextParser(testElem)
end = time.time()
print "Analysis complete.\n"
print "Context Element Analysis Time:" + str(end - start)

try:
    print "Assertions passed."
except AssertionError:
    print "Assertions Failed."

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
rand_array = np.random.randint(0, len(train_data.keys())-1, size=breakpoint)
train_keys = train_data.keys()
test_array = []
for i in rand_array:
    test_array.append(train_keys[i])

for test_inst in test_array:
    print "Element " + str(count)
    count += 1

    contextElem = train_data[test_inst]['context']
    target = train_data[test_inst]['target']
    if type(target) != None:
        [bestID, metricTracker] = main.processElem(contextElem, target, Dict)

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