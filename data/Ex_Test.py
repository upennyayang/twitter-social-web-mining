import os


path = '/Users/oliverfengpet/Dropbox/TwitterAffect/code/crawler/twitteraffect/delimited_data/Test/'
folder = 'Sad_etal'


targetPath = '/Users/oliverfengpet/Dropbox/TwitterAffect/Data/'
targetFolder = 'Testing'

target_file = 'Test_Sad.txt'


l = []
tf = open(targetPath+targetFolder+'/'+target_file,'w+')
for f in os.listdir(path+folder):
	if(f.find('.DS_Store')!=-1):
		continue
	of = open(path+folder+'/'+f,'r')
	
	for line_num, line in enumerate(of.readlines()):
		line = line.replace('\n','[newLine]')
		if(line.find(':tfdasb:')!=-1):
			line = line.replace(':tfdasb:','')
		if(line.find(':endcc:')!=-1):
			line = line.replace(':endcc:','')
			if(line in l):
				continue
			l.append(line)
			line = line.replace('[newLine]','')
			tf.write(' '+line+'\n');
			#tf.write(' afraid'+'\n')
		else:
			if(line not in l):
				l.append(line)
				tf.write(' '+line)
	
