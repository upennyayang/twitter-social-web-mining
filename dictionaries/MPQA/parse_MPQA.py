pos_list=set()
neg_list=set()

for line in open("/project/cis/nlp/data/corpora/mpqa-lexicon/subjclueslen1-HLTEMNLP05.tff"):
	words=line.split()
	if words[-1].endswith('negative'):
		#print words[2]
		neg_list.add(words[2].split('=')[1])
	elif words[-1].endswith('positive'):
		pos_list.add(words[2].split('=')[1])

#print neg_list
outfile_neg=open("mpqa_neg.txt",'w')
for word in neg_list:
	outfile_neg.write("%s\n" % word)
outfile_neg.close()

outfile_pos=open("mpqa_pos.txt",'w')
for word in pos_list:
	outfile_pos.write("%s\n" % word)
outfile_pos.close()
