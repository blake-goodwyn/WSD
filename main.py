__author__ = 'Richard Goodwyn'
import dataReader
import os
import contextHandler

refDict = ''  #input statement for reference dictionary
### Reference Dictionary Structure ###
# refDict[(word to be defined)] ==> sub-dictionary, keys == senseIDs
# refDict[(word to be defined)][senseID] ==> sense definition of given word

testSet = os.path.join("C:\Users\Blake Goodwyn\Documents\Code\cs4740p2\Atlassian_Repo","training-data.xml")  #data set to train
dataReader.read(testSet)

###Form array of instance elements with associated information
##->instance
##--->answer
##--->context

instanceArray = {}

for i in instanceArray.keys():
    answer = instanceArray[i].answer
    contextElem = instanceArray[i].context
    [contextArray, essentialWords, phraseArray, t_idx] = contextHandler.contextParser(contextElem)
    [preTarget,postTarget,target] = contextHandler.contextListHandler(phraseArray, t_idx)

    ###Definition scoring

    ##Determine
    targetGlossArray = []
    defnArray = refDict[target]