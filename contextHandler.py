__author__ = 'Richard Goodwyn'

import nltk
import copy
import wordGloss
import numpy as np
import nltk.corpus as corpus
import time
import gc

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
            preTarget = contextArray[0:target_idx]
            preTarget.reverse()
            preTarget = wordFilter(preTarget)
            postTarget = wordFilter(contextArray[target_idx+7:]) #index corresponding to after '>' of '</head>'
            check = False

    return preTarget, postTarget


def wordFilter(wordList, add=True):
#filters out nonessential words from the context in order to ensure that scoring
# only reflects relevant contextual words rather than all words

    array_copy = copy.copy(wordList)
    stopwords = nltk.corpus.stopwords.words('English')
    if add:
        additionalStopWords = ['(',')',',','.',':','"','?','!','*','(',')']
        stopwords.extend(additionalStopWords) #make stop words list more robust
    nonStopWords = [w for w in array_copy if w.lower() not in stopwords] #all words that are not stopWords

    if add:
        if len(nonStopWords) > 12:
            nonStopWords = nonStopWords[:11]

    return nonStopWords


def compIterator(contextArray, targetGlossArray, metricTracker, stopwords, ramp_down):
#Given the array of significant contextual words and the array of sense definitions,
#scores the senseIDs based on comparison of the sense definitions to the definitions of the contextual words
    #gc.enable()
    i = 0
    total = time.time()
    check = total
    for thing in contextArray:  #context words
        i += 1
        scale = np.power(ramp_down, i)
        glossArray = wordGloss.lookup(thing) #formation of synset for context word (WordNet)
        start = time.time()
        for j in sorted(targetGlossArray.keys()):  #definition of given senseIDs of target word, sorted due to likeliness of first sense
            dictDef = targetGlossArray[j]['-gloss']
            check = start
            for gloss_def in glossArray:  #each definition in synset
                overlap = 0
                for word in dictDef:
                    if word in gloss_def:
                        if word not in stopwords:
                            overlap += 1.0
                            metricTracker[j] += overlap/scale
                            check = time.time()
                    if (check - start) > .25:
                        break
                if (check - start) > .25:
                    break
        if (check - total) > 5:
            break




    return metricTracker
