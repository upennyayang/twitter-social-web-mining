import sys
import os
import string
import re

import codecs
from ttp import ttp
#p=ttp.Parser()

reload(sys)
sys.setdefaultencoding('utf-8')


def replace_text(ori,parseRes):
	result=ori
	for user in parseRes.users:
		result=result.replace('@'+user,'@[someUSER]')
	for tag in parseRes.tags:
		result=result.replace('#'+tag,'#[someTAG]')
	for url in parseRes.urls:
		result=result.replace(url,'[someURL]')
	return result


if len(sys.argv)<2 or len(sys.argv)>3:
	print 'Usage: python raw_to_delimited.py folderName'
	sys.exit()
folderName=str(sys.argv[1])
print folderName

replace_all=0
if len(sys.argv)==3:
	replace_all=int(sys.argv[2])
print replace_all


p=ttp.Parser()
sourceDir=folderName
targetDir=folderName.split(os.sep)[-1]
if not os.path.exists(targetDir):
	os.makedirs(targetDir)
#os.chdir(targetDir)
for fn in os.listdir(sourceDir):
	if replace_all==0 and os.path.exists(os.sep.join([targetDir,fn+'.delimited'])):
		continue
	print fn
	#ori_tweets=[]
	delimited_tweets=[]
	#cur_tweent
	#f=open(os.sep.join([sourceDir,fn]),'r')
	f=codecs.open(os.sep.join([sourceDir,fn]),encoding='utf-8',mode='r')
	lines=f.readlines()
	f.close()
	for i in range(0,len(lines)-1):
		if lines[i].startswith(':ccdasb:'):
			cur_tweet=lines[i][8:]
			while not cur_tweet.endswith(':endft:\n'):
				#print cur_tweet
				i+=1
				cur_tweet=''.join([cur_tweet,lines[i]])
			cur_tweet=cur_tweet[:-8]
			#ori_tweets.append(cur_tweet)
			#parseResult=p.parse(cur_tweet)
			#print cur_tweet
			delimited_tweets.append(replace_text(cur_tweet,p.parse(cur_tweet,False)))
			#print 'done'
	#f=open(os.sep.join([targetDir,fn+'.delimited']),'w')
	f=codecs.open(os.sep.join([targetDir,fn+'.delimited']),encoding='utf-8',mode='w')
	for tweet in delimited_tweets:
		f.write(':tfdasb:%s:endcc:\n' %tweet)
	f.close()


