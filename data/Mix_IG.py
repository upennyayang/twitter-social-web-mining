# 
# svm_save_model('libsvm.model', m)
# m = svm_load_model('libsvm.model')
import re
from nltk.tokenize import sent_tokenize
import sys
from nltk.corpus import PlaintextCorpusReader
#sys.path.append('/Users/oliverfengpet/Program/nlp/python_parser/no_index/libsvm-3.12/python/')
sys.path.append('/Users/oliverfengpet/Dropbox/TwitterAffect/liblinear-1.93/python')
from nltk.tokenize import word_tokenize
from progressbar import *
import emoticons
from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()
import textgain
import operator
from nltk import bigrams
from liblinearutil import *
import emowords
Training_Path = "/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Training"
Testing_Path = "/Users/oliverfengpet/Dropbox/TwitterAffect/Data/Testing"
TFIDF_Path = "/Users/oliverfengpet/Dropbox/TwitterAffect/TFIDF_RAW.txt"


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
		#sentences[i] = sentences[i].decode('utf-8','ignore')	
		#k = p.findall(sentences[i])
		k=word_tokenize(sentences[i])
		g = re.finditer(emoticons.Emoticon_RE,sentences[i])
		for ma in g:
			k.append(ma.group())
		for j in range(0, len(k)):
			k[j] = st.stem(k[j])
			if k[j] not in a:
				a[k[j]]=len(a)
	return a


def create_feature_space_IG(bi):
	a={}
	ig, gr, si = textgain.compute('IG')
	sortedIG = sorted(ig,key=ig.__getitem__,reverse=True)
	ki = sortedIG[:8000]
	k = bi[:16000]
	
	k.extend(ki)
	print len(k)
	
	for j in range(0,len(k)):
		if k[j] not in a:
			a[k[j]] = len(a)
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

def load_bi(path):
	result=[]
	f = open(path)
	for line_num, line in enumerate(f.readlines()):
		result.append(line.split()[0])
	
	return result

def vectorize(feature_space, sentence):
	k = word_tokenize(sentence)
	g = re.finditer(emoticons.Emoticon_RE,sentence)
	for i in range(0,len(k)):
		k[i] = st.stem(k[i])
	
	kb = bigrams(k)

	nk=[]	
	for b in kb:
		nk.append(b[0]+'_'+b[1])
	
	
	for ma in g:
		k.append(ma.group())
	
	k.extend(nk)
	#print k
	
	
	result = []
	result = [0] * len(feature_space)
	for key in feature_space:
		if key in k:
			result[feature_space[key]]+=1
		else:
			result[feature_space[key]]=0
	return result
	

def Training(directory,bi):
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
	# -b proba	lity_estimates: whether to train a SVC or SVR model for probability estimates, 0 or 1 (default 0)
	# -wi weight: set the parameter C of class i to weight*C, for C-SVC (default 1)

	#The k in the -g option means the number of attributes in the input data.
	vectors = []
	labels = []
	sentences = load_collection_sentence(directory)
	feature_space = create_feature_space_IG(bi)
	#print feature_space
	# try:
	#    with open('libsvm_SVC_Present.model'): 
	# 		m = svm_load_model('libsvm_SVC_Present.model')
	# 		return [m,feature_space]
	# except IOError:
	#    print 'Start Training Over.'
	
	count = 0
	for f in os.listdir(directory):
		of = open(directory+'/'+f,'r')
		count+=len(of.readlines())
	widgets = ['Train_Vectorize: ', Percentage(), ' ', Bar(marker='=',left='[',right=']'),
		        ' ', ETA(), ' ', FileTransferSpeed()]
	pbar = ProgressBar(widgets=widgets, maxval=count)
	pbar.start()
	curCount = 0
	for f in os.listdir(directory):
		of = open(directory+'/'+f,'r')
		for line_num, line in enumerate(of.readlines()):
			vector = vectorize(feature_space,line)
			vector.extend(emowords.getEWcnt(line,'0001'))
			vectors.append(vector)
			labels.append(label_map[f])
			pbar.update(curCount)
			curCount+=1
			#print label_map[f]
			#print line
	
	pbar.finish()
	prob  = problem(labels, vectors)
	param = parameter('-s 0')
	m1 = train(prob, param)
	#m1 = svm_train(labels, vectors, '-s 0 -t 0')
	save_model('libsvm_SVC_Mix.model', m1)
	return [m1,feature_space]

def Testing(directory,m1,feature_space):
	vectors = []
	labels = []
	count = 0
	for f in os.listdir(directory):
		of = open(directory+'/'+f,'r')
		count+=len(of.readlines())
	widgets = ['Test_Vectorize: ', Percentage(), ' ', Bar(marker='=',left='[',right=']'),
			        ' ', ETA(), ' ', FileTransferSpeed()]
	pbar = ProgressBar(widgets=widgets, maxval=count)
	pbar.start()
	
	curCount=0
	for f in os.listdir(directory):
		of = open(directory+'/'+f,'r')
		for line_num, line in enumerate(of.readlines()):
			vector = vectorize(feature_space,line)
			vector.extend(emowords.getEWcnt(line,'0001'))
			#print vector
			vectors.append(vector)
			#print test_label_map[f]
			labels.append(test_label_map[f])
			pbar.update(curCount)
			curCount+=1
	
	pbar.finish()
	m, p_acc, p_vals = predict(labels, vectors, m1)
	
	
	cm={}
	
	for i in range(0,5):
		cm[i]={}
		for j in range(0,5):
			cm[i][j]=0
	
	
	for i in range(0,len(m)):
		cm[labels[i]][m[i]]+=1
	
	
	print cm
	return [m,p_acc,p_vals]


def createWordCount(src,dest):
	for f in os.listdir(src):
		dicCount = {}
		of = open(src+'/'+f)
		df = open(dest+'/'+f,'w')
		for line_num, line in enumerate(of.readlines()):
			k = word_tokenize(line)
			for i in range(0,len(k)):
				k[i] = st.stem(k[i])
			
			k = bigrams(k)
			g = re.finditer(emoticons.Emoticon_RE,line)
			for ma in g:
				k.append((ma.group(),' '))
				#print k
			for w in k:
				if w in dicCount:
					dicCount[w]+=1
				else:
					dicCount[w]=1
		for key, value in dicCount.iteritems():
			if len(key)>1:
				df.write(key[0]+'_'+key[1]+' '+str(value))
			else:
			#	print 'he'
				df.write(key+' '+str(value))
			df.write('\n')
		df.close()
		of.close()

# bi = load_bi('/Users/oliverfengpet/Dropbox/TwitterAffect/IG_Bigram.txt')
# 
# [m, fs] = Training(Training_Path, bi)
# Testing(Testing_Path,m,fs)	
#print textgain.compute('IG')
#create_feature_space_IG(n)
#createWordCount(Training_Path,"/Users/oliverfengpet/Dropbox/TwitterAffect/IG_Bi/")
# for i in range(12,30):
# 	print 'The number of feature is '+ str(i*2000)
# 	[m, fs] = Training(Training_Path,i*2000, bi)
# 	Testing(Testing_Path,m,fs)


# vector = vectorize(fs," I hate when people have candy in their mouth and they are moving it around and you can hear that nasty spit noise. #[someTAG] #[someTAG]")
# label = [0]
# vectors = []
# vectors.append(vector)	
# svm_predict(label, vectors, m)	
	
	
