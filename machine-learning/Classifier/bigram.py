#
# svm_save_model('libsvm.model', m)
# m = svm_load_model('libsvm.model')
import re
from nltk.tokenize import sent_tokenize
import sys
from nltk.corpus import PlaintextCorpusReader
sys.path.append('/Users/Alantyy/Dropbox/TwitterAffect/libsvm-3.17/python/')
from svmutil import *
from nltk.tokenize import word_tokenize
import twokenize
from nltk import bigrams
from progressbar import *

Training_Path = "/Users/Alantyy/Dropbox/TwitterAffect/Data/Training"
Testing_Path = "/Users/Alantyy/Dropbox/TwitterAffect/Data/Testing"
TFIDF_Path = "/Users/Alantyy/Dropbox/TwitterAffect/TFIDF_RAW.txt"


label_map ={'Training_Happy.txt':1,'Training_Angry.txt':0,'Training_Sad.txt':2,'Training_Ashamed.txt':3,'Training_Afraid.txt':4}
test_label_map ={'Test_Happy.txt':1,'Test_Angry.txt':0,'Test_Sad.txt':2,'Test_Ashamed.txt':3,'Test_Afraid.txt':4}


def load_collection_sentence(directory):
	# files_all = PlaintextCorpusReader(directory,'.*')
	# print files_all
	# result = sent_tokenize(files_all.raw().lower())
	# print result
	result = []
	for f in os.listdir(directory):
		of = open(directory+'/'+f,'r')
		for line in of.readlines():
			result.append(line.lower())
	#print len(result)
	return result

def create_feature_space(sentences):
	a={}
	#p = re.compile('\w+')
	for i in range(0,len(sentences)):
		#sentences[i] = sentences[i].decode('utf-8')

		#k = p.findall(sentences[i])
		#sentences[i] = sentences[i].encode('utf-8')
		#sentences[i] = u" ".join(twokenize.tokenize(sentences[i])).encode('utf-8')
		k=word_tokenize(sentences[i])
		k = bigrams(k)
		#k = sentences[i].split()
		for j in range(0, len(k)):
			if k[j] not in a:
				a[k[j]]=len(a)
	return a


def create_featuer_space_TFIDF(file):
	a={}
	f = open(file)
	for line in f.readlines():
		line = line.replace("'","")
		k=line.split(',')
		for j in range(0, len(k)):
			k[j] = k[j].strip()
			if k[j] not in a:
				a[k[j]]=len(a)
	return a

def vectorize(feature_space, sentence):
#	sentence = u" ".join(twokenize.tokenize(sentence)).encode('utf-8')
	k = word_tokenize(sentence)
	k = bigrams(k)
	#k=sentence.split()
	result = []
	result = [0] * len(feature_space)
	for key in feature_space:
		if key in k:
			result[feature_space[key]]+=1
		else:
			result[feature_space[key]]=0
	return result


def Training(directory):
	# -s svm_type : set type of SVM (default 0)
	# 	0 -- C-SVC
	# 	1 -- nu-SVC
	# 	2 -- one-class SVM
	# 	3 -- epsilon-SVR
	# 	4 -- nu-SVR
	# -t kernel_type : set type of kernel function (default 2)
	# 	0 -- linear: u'*v
	# 	1 -- polynomial: (gamma*u'*v + coef0)^degree
	# 	2 -- radial basis function: exp(-gamma*|u-v|^2)
	# 	3 -- sigmoid: tanh(gamma*u'*v + coef0)
	# -d degree : set degree in kernel function (default 3)
	# -g gamma : set gamma in kernel function (default 1/num_features)
	# -r coef0 : set coef0 in kernel function (default 0)
	# -c cost : set the parameter C of C-SVC, epsilon-SVR, and nu-SVR (default 1)
	# -n nu : set the parameter nu of nu-SVC, one-class SVM, and nu-SVR (default 0.5)
	# -p epsilon : set the epsilon in loss function of epsilon-SVR (default 0.1)
	# -m cachesize : set cache memory size in MB (default 100)
	# -e epsilon : set tolerance of termination criterion (default 0.001)
	# -h shrinking: whether to use the shrinking heuristics, 0 or 1 (default 1)
	# -b probability_estimates: whether to train a SVC or SVR model for probability estimates, 0 or 1 (default 0)
	# -wi weight: set the parameter C of class i to weight*C, for C-SVC (default 1)

	#The k in the -g option means the number of attributes in the input data.
	vectors = []
	labels = []
	sentences = load_collection_sentence(directory)
	feature_space = create_feature_space(sentences)
	print "feature space created"


	count = 0
	for f in os.listdir(directory):
		of = open(directory+'/'+f,'r')
		count+=len(of.readlines())
	widgets = ['Train_Vectorize: ', Percentage(), ' ', Bar(marker='0',left='[',right=']'),
		        ' ', ETA(), ' ', FileTransferSpeed()]
	pbar = ProgressBar(widgets=widgets, maxval=count)
	pbar.start()
	# try:
	#    with open('libsvm_SVC_Present.model'):
	# 		m = svm_load_model('libsvm_SVC_Present.model')
	# 		return [m,feature_space]
	# except IOError:
	#    print 'Start Training Over.'
	curCount = 0
	for f in os.listdir(directory):
		of = open(directory+'/'+f,'r')
		for line_num, line in enumerate(of.readlines()):
			vector = vectorize(feature_space,line)
			vectors.append(vector)
			labels.append(label_map[f])
			pbar.update(curCount)
			curCount+=1
			#print label_map[f]
			#print line

	pbar.finish()
	m1 = svm_train(labels, vectors, '-s 0 -t 0')
	svm_save_model('libsvm_SVC_emoticon_bigrams.model', m1)
	return [m1,feature_space]

def Testing(directory,m1,feature_space):
	vectors = []
	labels = []

	count = 0
	for f in os.listdir(directory):
		of = open(directory+'/'+f,'r')
		count+=len(of.readlines())
	widgets = ['Test_Vectorize: ', Percentage(), ' ', Bar(marker='0',left='[',right=']'),
			        ' ', ETA(), ' ', FileTransferSpeed()]
	pbar = ProgressBar(widgets=widgets, maxval=count)
	pbar.start()

	curCount=0
	for f in os.listdir(directory):
		of = open(directory+'/'+f,'r')
		for line_num, line in enumerate(of.readlines()):
			vector = vectorize(feature_space,line)
			#print vector
			vectors.append(vector)
			#print test_label_map[f]
			labels.append(test_label_map[f])
			pbar.update(curCount)
			curCount+=1
	pbar.finish()
	#print "get here"
	m, p_acc, p_vals = svm_predict(labels, vectors, m1)

	print m
	return [m,p_acc,p_vals]


[m, fs] = Training(Training_Path)
Testing(Testing_Path,m,fs)
# vector = vectorize(fs," I hate when people have candy in their mouth and they are moving it around and you can hear that nasty spit noise. #[someTAG] #[someTAG]")
# label = [0]
# vectors = []
# vectors.append(vector)
# svm_predict(label, vectors, m)


