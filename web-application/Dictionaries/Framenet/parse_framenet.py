import sys
print sys.argv
if len(sys.argv)<2:
	print "insufficient parameters"
	sys.exit()

emo_list=set()
infile=sys.argv[1]
for line in open(infile,'r'):
	for word in line.split(','):
		if word.find('_')!=-1 or word.find('(')!=-1:
			continue
		else:
			emo_list.add(word.split('.')[0].replace(' ',''))

outfile=open("list_emotions",'w')
for word in emo_list:
	outfile.write("%s\n" %word)
outfile.close()
