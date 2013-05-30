from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import math
import os
import operator


def load_file_tokens(filepath):
	inputFile = open(filepath,'r')
    	fileContentsLower = inputFile.read().lower()
    	result = word_tokenize(fileContentsLower)
	return result


def PMI(directory):
	happy = 'Training_Happy.txt'
	sad = 'Training_Sad.txt'
	ashamed = 'Training_Ashamed.txt'
	angry = 'Training_Angry.txt'
	afraid = 'Training_Afraid.txt'
	
	listFiles = [happy,sad,ashamed,angry,afraid]
	femotion = {}
	
	for f in listFiles:
		rawContents = load_file_tokens(directory+'/'+f)
		fdist = FreqDist( rawContents )
		femotion[f] = fdist
	
	countEmotions = {}
	
	for f in listFiles:
		of = open(directory+'/'+f,'r')
		countEmotions[f]=len(of.readlines())
		of.close()
	
	countAll={}
	counted={}
	for f in listFiles:
		for key in femotion[f].keys():
			for key_file in femotion.keys():
				if(key in femotion[key_file].keys() and (key not in counted.keys())):
					if key in countAll:
						countAll[key]+=femotion[key_file][key]
					else:
						countAll[key]=femotion[key_file][key]
			
			counted[key]=True
	
	coutWords=0
	for f in listFiles:
		coutWords+=countEmotions[f]
	
	
	
	PMI={}
	
	for f in listFiles:
		PMI[f]={}
		for key in femotion[f].keys():
			PMI[f][key] = math.log(float(femotion[f][key])/float(countEmotions[f])/(float(countAll[key])/float(coutWords)))
	
	sortedEmotions = {}	
	for f in listFiles:
		sortedEmotions[f] = sorted(PMI[f].iteritems(),key=operator.itemgetter(1),reverse=True)
	for f in listFiles:
		print f
		print sortedEmotions[f][:100]

PMI("/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training")
				
				
	