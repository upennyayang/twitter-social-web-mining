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

def get_top_words(directory, n, file):
	num_docs = 0.0
	flist = {}
	result = {}
	for f in os.listdir(directory):
		#stop = "/Users/oliverfengpet/Dropbox/TwitterAffect/stoplist.txt"
		
		num_docs+=1
		rawContents = load_file_tokens(directory+'/'+f)
		fdist = FreqDist( rawContents )
		normalF = max(fdist.values())
		
		for key in fdist.keys():
			fdist[key]=float(float(fdist[key])/normalF)
	
		flist[directory+'/'+f] = fdist
		
		
	for key in flist[file].keys():
		num_appear=0
		for key_file in flist.keys():
			if key in flist[key_file].keys():
				num_appear+=1
		
		result[key] = flist[file][key]*math.log(num_docs/(num_appear))
	
	sorted_x = sorted(result.iteritems(), key=operator.itemgetter(1),reverse=True)
	
	top_x = sorted_x[:n]
	result = []
	
	for item in top_x:
		result.append(item[0])
	
	return result
	
		
print get_top_words("/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training",100,"/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training/Training_Afraid.txt")
print get_top_words("/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training",100,"/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training/Training_Happy.txt")
print get_top_words("/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training",100,"/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training/Training_Sad.txt")
print get_top_words("/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training",100,"/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training/Training_Ashamed.txt")
print get_top_words("/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training",100,"/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training/Training_Angry.txt")
# my_tfidf = tfidf.TfIdf("/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training/Training_Happy.txt","/Users/oliverfengpet/Dropbox/TwitterAffect/stoplist.txt")
# 
# f=open("/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training/Training_Afraid.txt",'r')
# my_tfidf.add_input_document(f.read())
# f.close()
# 
# f=open("/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training/Training_Sad.txt",'r')
# my_tfidf.add_input_document(f.read())
# f.close()
# 
# f=open("/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training/Training_Ashamed.txt",'r')
# my_tfidf.add_input_document(f.read())
# f.close()
# 
# f=open("/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training/Training_Angry.txt",'r')
# my_tfidf.add_input_document(f.read())
# f.close()
# 
# print my_tfidf.get_num_docs()

	
#print get_top_words_with_stoplist('/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training',200)
