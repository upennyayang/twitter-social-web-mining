import sys
print sys.argv
if len(sys.argv)<2:
	print "insufficient parameters"
	sys.exit()
infile=sys.argv[1]
f=open(infile,'r')
lines=f.readlines()
f.close()
f=open('list_'+infile,'w')
for line in lines[35:]:
	f.write(line)
f.close()
