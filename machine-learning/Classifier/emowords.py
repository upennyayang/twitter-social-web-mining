import sys
import os
import operator
from collections import Counter as mset
from nltk.tokenize import word_tokenize

dicDir="./Dictionaries"
blDIR=os.sep.join([dicDir,"Bingliu"])
fmnDIR=os.sep.join([dicDir,"Framenet"])
mpqaDIR=os.sep.join([dicDir,"MPQA"])
wnDIR=os.sep.join([dicDir,"Wordnet"])

Max_ch=7
bl_neg_list=open(os.sep.join([blDIR,"list_negative-words.txt"])).readlines()
bl_neg_list=[word.rstrip('\n') for word in bl_neg_list]
bl_neg_cnt=mset(bl_neg_list)
for i in range(1,Max_ch):
	bl_neg_cnt+=bl_neg_cnt

bl_pos_list=open(os.sep.join([blDIR,"list_positive-words.txt"])).readlines()
bl_pos_list=[word.rstrip('\n') for word in bl_pos_list]
bl_pos_cnt=mset(bl_pos_list)
for i in range(1,Max_ch):
	bl_pos_cnt+=bl_pos_cnt


fmn_emo_list=open(os.sep.join([fmnDIR,"list_emotions.txt"])).readlines()
fmn_emo_list=[word.rstrip('\n') for word in fmn_emo_list]
fmn_emo_cnt=mset(fmn_emo_list)
for i in range(1,Max_ch):
	fmn_emo_cnt+=fmn_emo_cnt


mpqa_neg_list=open(os.sep.join([mpqaDIR,"list_negative.txt"])).readlines()
mpqa_neg_list=[word.rstrip('\n') for word in mpqa_neg_list]
mpqa_neg_cnt=mset(mpqa_neg_list)
for i in range(1,Max_ch):
	mpqa_neg_cnt+=mpqa_neg_cnt

mpqa_pos_list=open(os.sep.join([mpqaDIR,"list_positive.txt"])).readlines()
mpqa_pos_list=[word.rstrip('\n') for word in mpqa_pos_list]
mpqa_pos_cnt=mset(mpqa_pos_list)
for i in range(1,Max_ch):
	mpqa_pos_cnt+=mpqa_pos_cnt


wn_anger_list=open(os.sep.join([wnDIR,"list_anger.txt"])).readlines()
wn_anger_list=[word.rstrip('\n') for word in wn_anger_list]
wn_anger_cnt=mset(wn_anger_list)
for i in range(1,Max_ch):
	wn_anger_cnt+=wn_anger_cnt

wn_disgust_list=open(os.sep.join([wnDIR,"list_disgust.txt"])).readlines()
wn_disgust_list=[word.rstrip('\n') for word in wn_disgust_list]
wn_disgust_cnt=mset(wn_disgust_list)
for i in range(1,Max_ch):
	wn_disgust_cnt+=wn_disgust_cnt

wn_fear_list=open(os.sep.join([wnDIR,"list_fear.txt"])).readlines()
wn_fear_list=[word.rstrip('\n') for word in wn_fear_list]
wn_fear_cnt=mset(wn_fear_list)
for i in range(1,Max_ch):
	wn_fear_cnt+=wn_fear_cnt

wn_joy_list=open(os.sep.join([wnDIR,"list_joy.txt"])).readlines()
wn_joy_list=[word.rstrip('\n') for word in wn_joy_list]
wn_joy_cnt=mset(wn_joy_list)
for i in range(1,Max_ch):
	wn_joy_cnt+=wn_joy_cnt

wn_sadness_list=open(os.sep.join([wnDIR,"list_sadness.txt"])).readlines()
wn_sadness_list=[word.rstrip('\n') for word in wn_sadness_list]
wn_sadness_cnt=mset(wn_sadness_list)
for i in range(1,Max_ch):
	wn_sadness_cnt+=wn_sadness_cnt


def getEWcnt(text,dic='1111',flag=0):
	#text_word=text.split()
	dic=int(dic,2)
	if int(flag)==0:
		text_word=word_tokenize(text)
	else:
		text_word=word_tokenize(text.decode('utf8'))
	text_word=[w.lower() for w in text_word]
	#print text_word
	text_cnt=mset(text_word)
	#print text_cnt
	#print wn_joy_cnt
	
	EWcnt={}
	EWcnt['bl_neg']=sum((text_cnt & bl_neg_cnt).values())
	EWcnt['bl_pos']=sum((text_cnt & bl_pos_cnt).values())
	EWcnt['fmn_emo']=sum((text_cnt & fmn_emo_cnt).values())
	EWcnt['mpqa_neg']=sum((text_cnt & mpqa_neg_cnt).values())
	EWcnt['mpqa_pos']=sum((text_cnt & mpqa_pos_cnt).values())
	EWcnt['wn_anger']=sum((text_cnt & wn_anger_cnt).values())
	EWcnt['wn_disgust']=sum((text_cnt & wn_disgust_cnt).values())
	EWcnt['wn_fear']=sum((text_cnt & wn_fear_cnt).values())
	EWcnt['wn_joy']=sum((text_cnt & wn_joy_cnt).values())
	EWcnt['wn_sadness']=sum((text_cnt & wn_sadness_cnt).values())

	EW=[]
	if (dic&8)>0:
		EW.append(EWcnt['bl_neg'])
		EW.append(EWcnt['bl_pos'])
	if (dic&4)>0:
		EW.append(EWcnt['fmn_emo'])
	if (dic&2)>0:
		EW.append(EWcnt['mpqa_neg'])
		EW.append(EWcnt['mpqa_neg'])
	if (dic&1)>0:
		EW.append(EWcnt['wn_anger'])
		EW.append(EWcnt['wn_disgust'])
		EW.append(EWcnt['wn_fear'])
		EW.append(EWcnt['wn_joy'])
		EW.append(EWcnt['wn_sadness'])
	
	#return EWcnt
	return EW
