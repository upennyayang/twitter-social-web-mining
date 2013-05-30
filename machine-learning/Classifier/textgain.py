#!/usr/bin/env python
'''Script to compute information gain, gain ration for words in documents
for a document base'''
__version__ = "1.0"
__date__ = "June 2012"
__author__ = "Vincent Van Asch"

import os, sys, getopt, time
from math import log

def loginfo(s): print >>sys.stderr, '%s: %s' %(time.strftime('%d/%m/%Y %H:%M:%S'), s)

def fread(fname, sep=None):
    with open(os.path.abspath(os.path.expanduser(fname)), 'rU') as f:
        for l in f:
            line = l.strip()
            if line: yield line.split()


class Data(dict):
    def __init__(self, d={}, source=None):
        dict.__init__(self, d)
        self._source = source
        
    @property
    def source(self):
        '''The folder on which this data object is based'''
        return self._source

def entropy(f):
    '''Takes a frequency and returns -1*f*log(f,2)'''
    return -1 * f * log(f,2)

def plain(fname):
    '''(expected format, for each line: token count)''' 
    for token, count in fread(fname):
        yield token, int(count)
        
def counter(fname):
    '''(expected format: space-separated tokens)''' 
    counts = {}
    
    for tokens in fread(fname):
        for token in tokens:
            counts[token] = counts.get(token, 0) + 1
        
    for token, count in counts.items():
        yield token, count
        

def compute(dir, reader=plain, verbose=False, crop=10, sortkey=1):
    '''Reads in the data files from dir into a dict'''
    # Get all files in the dir
    dir = os.path.abspath(os.path.expanduser(dir))
    fnames = [os.path.join(dir, n) for n in os.listdir(dir) if not n.startswith('.')]
    if verbose: loginfo("Found %d files in %s" %(len(fnames), dir))
    
    total = float(len(fnames))
    
    labels = {}
    data = Data(source = dir)
    if verbose: loginfo('First round...')
    cc=0
    for fname in fnames:        
        # Create a class label
        label = os.path.basename(fname).split('.')[0]
        labels[label] = labels.get(label, 0) + 1

        # Read in all counts
        for token, count in reader(fname):
            if token in data.keys():
                if count in data[token].keys():
                    data[token][count][0] += 1
                    data[token][count][1][label] = data[token][count][1].get(label, 0) + 1  
                else:
                    data[token][count] = [1, {label:1}]
            else:
                data[token] = {count:[1, {label:1}]}
                
        cc+=1
        if verbose: sys.stderr.write('Read %d/%d\r' %(cc, total))
    if verbose: print >>sys.stderr, 'Read %d/%d' %(cc, total)
    # Insert all zero counts
    cc=0
    if verbose: loginfo('Second round...')
    for fname in fnames:
        # Create a class label
        label = os.path.basename(fname).split('.')[0]      

        tokens=set()
        for token, count in reader(fname):
            tokens.add(token)

        # Get tokens in data that are not in this file
        zero_features = set(data.keys()).difference(tokens)
        
        # Add them to data
        count = 0
        for token in zero_features:
            if count in data[token].keys():
                data[token][count][0] += 1
                data[token][count][1][label] = data[token][count][1].get(label, 0) + 1  
            else:
                data[token][count] = [1, {label:1}]
            
        cc+=1
        if verbose: sys.stderr.write('Read %d/%d\r' %(cc, total))
    print >>sys.stderr, 'Read %d/%d' %(cc, total)
                
    # Counts
    nfeatures = float(len(data)) 
    nlabels = float(len(labels))
    
    if verbose: loginfo("Found %d tokens" %nfeatures)
    if verbose: loginfo("Found %d class labels" %nlabels)
    
    # Database entropy H(C)
    HC = 0.0
    for cl, count in labels.items():
        freq = count/total
        HC += entropy(freq)

    # The weights
    IG = {}
    GR = {}
    SI = {}
    
    for feature, counts in data.items():        
        si = 0.0
        ch  = 0.0
        for fv, clist in counts.items():
            fvcount, clcounts = clist
            fvcount = float(fvcount)
            
            # Calculate H(C|vi)
            hcv = 0.0
            for cl, c in clcounts.items():
                cfreq = c / fvcount
                hcv += entropy(cfreq)
                
            # Calculate split values
            freq = fvcount / total
            si += entropy(freq)
            
            # Calculate conditional entropy -1*P(vi)*H(C|vi)
            ch += (-1 * freq * hcv )
        
        
        # Information gain
        ig = HC + ch
        
        # Gain ratio
        if si == 0:
            gr = 0.0
        else:
            gr = ig / si
            
        # Store
        IG[feature] = ig
        GR[feature] = gr
        SI[feature] = si
            
    format(IG, GR, SI, source=data, labels=labels, crop=crop, sortkey=sortkey)
    
    return IG, GR, SI
    
            
def getlabelcount(token, data, labels):
    out = {}
    for label in labels:
        som=0
        for count, clist in data.items():
            som += count * clist[1].get(label, 0)
        out[label] = som
    
    keys = out.keys()
    keys.sort()
    ss=[]
    for k in keys:
        ss.append('%s:%-4d' %(k, out[k]))
    
    return ' '.join(ss)
    
    
            
def format(ig, gr, si, sortkey=1, crop=10, source=None, labels=None):
    '''Print the lists'''    
    data=[]
    for f in ig.keys():
        data.append((f, ig[f], gr[f], si[f]))
    data.sort(key = lambda x:x[sortkey], reverse=True)
    
    end='...'
    if not crop or (len(data) <= 2*crop):
        crop = len(data)
        end=''
    
    print '%-10s\t%8s\t%8s\t%8s\t%s'  %('Feat', 'InfoGain','GainRat', 'SplitInf', 'count(label|feat)')
    f='%-10s\t%8f\t%8f\t%8f'
    for d in data[:crop]:
        info = getlabelcount(d[0], source[d[0]], labels)
        print (f %d), '\t', info 
        
    if end:
        print end
        for d in data[len(data)-crop:]:
            info = getlabelcount(d[0], source[d[0]], labels)
            print (f%d),'\t', info
        


READERS = [plain, counter]
def _usage():
    readerstring = []
    for i,r in enumerate(READERS):
        readerstring.append(' '*12 + '%2d : %-8s %s' %(i, r.func_name, r.func_doc))
    readerstring = '\n'.join(readerstring)
    print >> sys.stderr, '''Compute information gain an gain ratio of tokens (version %s)
    
This script can be used on a collection of documents. For each token in each document
the Information Gain and Gain Ratio is printed to STDOUT. 
    
USAGE
    $ python textgain.py [-c int] [-v] [-r int] [-s int] dir 
    
     dir  : a folder with files. Each file should have the naming format:
            classlabel.xxx. The xxx-part is not used in the script, but is needed to 
            create more files for the same class label. Class labels should not
            contain a ".". The format of the files depends in the reader that is
            used (see -r option).

OPTIONS
    -r int: Specify the reader to use:
%s
    -c int: crop the output to int tokens at the top, and int tokens
            at the bottom. If int is 0, everything is reported. (default: 10)
    -s int: sort on:
             0 : Feature
             1 : InfoGain
             2 : Gain Ratio
             3 : Split Info
    -v : print more info
    
ACKNOWLEDGEMENTS
    Based on the information in the Timbl reference guide.
    http://ilk.uvt.nl/timbl

%s, %s''' %(__version__, readerstring, __author__, __date__)

if __name__ == '__main__':

    try:
        opts,args=getopt.getopt(sys.argv[1:],'hvr:c:s:', ['help'])
    except getopt.GetoptError:
        # print help information and exit:
        _usage()
        sys.exit(2)
        
    verbose = False
    reader = plain
    crop = 10
    sortkey = 1
    
    for o, a in opts:
        if o in ('-h', '--help'):
            _usage()
            sys.exit()
        if o == '-v':
            verbose = True
        if o == '-r':
            reader = READERS[int(a)]
        if o == '-c':
            crop = int(a)
        if o == '-s':
            sortkey = int(a)
            
    if len(args) != 1:
        _usage()
        sys.exit(1)
            
    if verbose:
        names = ['Feature', 'InfoGain', 'Gain Ratio', 'Split Info']
        loginfo('Using function "%s" to read in files' %(reader.func_name))
        loginfo('Sorting output on %s' %names[sortkey])
        if crop: loginfo('Cropping output to %d features' %(2*crop))
          
    compute(args[0], reader = reader, verbose=verbose, crop=crop, sortkey = sortkey)