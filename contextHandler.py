__author__ = 'Richard Goodwyn'

import nltk
import copy

def contextParser(contextElem):
#tokenizes and parses through context element.
# Returns array of all tokens, array of critical words, array of tuples with critical word phrases,
#  and the index of the target word in the critical word array

    #Tokenize context element
    contextArray = nltk.word_tokenize(contextElem)

    #Locate target word in contextArray and remove <head> tags
    target = ""
    target_idx = 0
    while target == "":
        if contextArray[target_idx] != "<":
            target_idx += 1
        else:
            if contextArray[target_idx+1] == "head":
                #obtain preliminary index
                temp = contextArray[target_idx+3]

                #assert tag locations
                assert contextArray[target_idx+1] == "head"
                assert contextArray[target_idx+5] == "/head"

                #delete tags from array
                del contextArray[target_idx:target_idx+3]
                del contextArray[target_idx+1:target_idx+4]

                #assert tag index preserved
                assert (temp == contextArray[target_idx])

                #assign target index
                target = contextArray[target_idx]

    #Perform Part-of-Speech Tagging and filter out non-essential words
    outArray, tupleList = wordFilter(contextArray,target_idx)

    #Locate target index in outArray
###############################################################
    ### This is inherently unreliable. Fix in the future. ###
    i = 0  #iterator
    while i < len(outArray):
        if outArray[i] == contextArray[target_idx]:
            target_idx_crit = i
            i = len(outArray)
        else:
            i += 1
###############################################################

    targetTuple = tuple([target_idx,target_idx_crit])

    return contextArray, outArray, tupleList, targetTuple

def contextListHandler(tuplesArray, target):
#Given a list of essential words, forms the pre- and post-context arrays about the target word.
# Returns preTarget array, postTarget array, and target word
    i = 0  #iterator
    t = 0  #tuple index
    while i < target[1]:
        i += len(tuplesArray[t])
        t += 1

    preContext = tuplesArray[0:t]
    postContext = tuplesArray[t+1:len(tuplesArray)]
    preContext.reverse()

    return preContext, postContext



def wordFilter(array,target):
    ## Given an input token array, filters out non essential words while preserving phrases
    array_copy = copy.copy(array)
    array_tagged = nltk.pos_tag(array_copy)
    outArray = []
    nonEssentials = ['(',')',',','--','.',':','CC','DT','IN','LS','MD','PDT','POS','RP','SYM','TO','WDT','WP','WP$','WRB','"']
    for i in range(0,len(array_copy)):
        if array_tagged[i][1] not in nonEssentials:
            outArray.append(array_copy[i])
        else:
            array_copy[i] = "<outted>"

    #forms tuples from initial array
    i = 0  #iterator1
    j = 0  #iterator2
    tupleList = []
    while i < len(array_copy):
        if i == target:
            tupleList.append(tuple([array_copy[i]]))
            i += 1
        if array_copy[i] != "<outted>":
            j = i
            while j < len(array_copy) and array_copy[j] != "<outted>":
                j += 1
            tupleList.append(tuple(array_copy[i:j]))
            i = j
        else:
            i += 1

    return outArray, tupleList