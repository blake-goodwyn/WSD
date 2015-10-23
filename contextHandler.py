__author__ = 'Richard Goodwyn'

import nltk
import copy
import wordGloss
import numpy as np
import time

def contextParser(contextElem):
#tokenizes and parses through context element, locates <head> tag and splits context
# element into two arrays, preTarget and postTarget, containing only contextually relevant words

    #Tokenize context element
    contextArray = nltk.word_tokenize(contextElem)

    #Locate target word in contextArray and remove <head> tags
    check = True
    target_idx = 0
    while check:
        if contextArray[target_idx] != "<":
            target_idx += 1
        else:
            preTarget = wordFilter(contextArray[0:target_idx])
            postTarget = wordFilter(contextArray[target_idx+7:])
            preTarget.reverse()
            check = False

    return preTarget, postTarget


def wordFilter(wordList):
#filters out nonessential words from the context in order to ensure that scoring
# only reflects relevant contextual words rather than all words

    array_copy = copy.copy(wordList)
    stopwords = nltk.corpus.stopwords.words('English')
    additionalStopWords = ['(',')',',','.',':','"','?','!','*','(',')']
    stopwords.extend(additionalStopWords) #make stop words list more robust
    nonStopWords = [w for w in array_copy if w.lower() not in stopwords] #all words that are not stopWords
    outArray = [] #list of all tokens but stopWords are replaced with <outted>

    #Add nonStopWords to outArray and update all stopWords in array_copy with '<outted>'
    for i in range(0,len(array_copy)):
        if array_copy[i] in nonStopWords:
            outArray.append(array_copy[i])

    return outArray


def compIterator(contextArray,targetGlossArray,metricTracker,ramp_down, stopwords):
#Given the array of significant contextual words and the array of sense definitions,
#scores the senseIDs based on comparison of the sense definitions to the definitions of the contextual words

    for i in range(0, len(contextArray)):  #pre-target word phrases
        for j in targetGlossArray.keys():  #definition of given senseIDs of target word
            dictDef = nltk.word_tokenize((targetGlossArray[j]['-gloss'] + " " + targetGlossArray[j]['-synset']))
            glossArray = wordGloss.lookup(contextArray[i]) #formation of synset for context word (WordNet)
            for gloss_def in glossArray:  #each definition in synset
                overlap = 0
                gloss_def = set(nltk.word_tokenize(gloss_def))  #definition, tokenized and filtered
                for word in dictDef:
                    if word not in stopwords: #condensed word filter
                        try:
                            gloss_def.remove(word)
                            overlap += 1.0
                        except KeyError:
                            overlap = overlap
                        metricTracker[j] += overlap/np.power(ramp_down, i)

    return metricTracker
