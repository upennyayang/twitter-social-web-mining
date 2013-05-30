import sys
print sys.argv
if len(sys.argv)<2:
	print "insufficient parameters"
	sys.exit()
words=[]
infile=sys.argv[1]
for line in open(infile,'r'):
	words.extend(line.split()[1:])
outfile=open('list_'+infile,'w')
for word in words:
	outfile.write("%s\n" %word)
outfile.close()

	
