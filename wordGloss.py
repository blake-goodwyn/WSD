__author__ = 'Blake Goodwyn'
from nltk.corpus import wordnet as WN
import nltk
import time

def lookup(word):

    defArray = WN.synsets(word)
    outArray = []
    for i in defArray:
        outArray.append(nltk.word_tokenize(str(i.definition())))

    return outArray

def auxGloss(word):

    defArray = WN.synsets(word)
    outDict = {}
    for i in defArray:
        outDict[i] = i.definition()

    return outDict
