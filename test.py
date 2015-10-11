__author__ = 'Richard Goodwyn'
import contextHandler
import time

testElem = "Do you know what it is ,  and where I can get one ?  We suspect you had seen the Terrex Autospade ,  which is made by Wolf Tools .  It is quite a hefty spade , with bicycle - type handlebars and a sprung lever at the rear , which you step on to <head>activate</head> it . Used correctly ,  you should n't have to bend your back during general digging ,  although it wo n't lift out the soil and put in a barrow if you need to move it !  If gardening tends to give you backache ,  remember to take plenty of rest periods during the day ,  and never try to lift more than you can easily cope with . "

print "Begin Context Element Test Analysis."
print "Gathering information..."
start = time.time()
[context, essentialWords, phraseArray, t_idx] = contextHandler.contextParser(testElem)
[preTarget,postTarget] = contextHandler.contextListHandler(phraseArray, t_idx)
end = time.time()
print "Analysis complete.\n"
print "Context Element Analysis Time:" + str(end - start)

print "\nPerforming Assertions."
try:

    assert(context[t_idx[0]] == essentialWords[t_idx[1]]) #target word index assertion
    assert(essentialWords[t_idx[1]-1] == preTarget[0][len(preTarget[0])-1]) #pre-target first word assertion
    assert(essentialWords[t_idx[1]+1]) == postTarget[0][0] #post-target first word assertion

    print "Assertions passed."
except AssertionError:
    print "Assertions Failed."
