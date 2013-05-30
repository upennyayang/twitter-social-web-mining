# Django webpage entrance for twitteraffect project.

from django.http import HttpResponse
import sys

root = "/Users/oliverfengpet/Dropbox/TwitterAffect"



sys.path.append(root)

import Mix_IG
import crawler
sys.path.append('/Users/oliverfengpet/Program/nlp/python_parser/no_index/libsvm-3.12/python/')
sys.path.append('/Users/oliverfengpet/Dropbox/TwitterAffect/liblinear-1.93/python')
from svmutil import *
from liblinearutil import *
# define (url -> python) mapping in urls.py

 # (r'^$', index.print_welcome)
 # http://127.0.0.1:8000/
happy_model = svm_load_model('libsvm_SVC_stem_emoticons_Happy.model')
sad_model = svm_load_model('libsvm_SVC_stem_emoticons_Sad.model')
ashamed_model = svm_load_model('libsvm_SVC_stem_emoticons_Ashamed.model')
angry_model = svm_load_model('libsvm_SVC_stem_emoticons_Angry.model')
afraid_model = svm_load_model('libsvm_SVC_stem_emoticons_Afraid.model')
model = load_model('libsvm_SVC_Mix.model')
bi = Mix_IG.load_bi("IG_Bigram.txt")
fs = Mix_IG.create_feature_space_IG(bi)
def print_welcome(request):
    html = "<html>" + get_style() + \
           "<body><div id=\"wrapper\">" \
           "CIS630 Project 2 - Twitter Affect" + \
           "<br>Tao Feng Shang CC le ya!" + \
           "<br><a href=\"crawler\">See Random Tweets Classification</a>" \
           "</div></body></html>"

    return HttpResponse(html)


#  (r'^crawler/$', index.print_crawling)
#   http://127.0.0.1:8000/crawler/

def print_crawling(request):
    # load
    print "hello"
    #model = load_model('libsvm_SVC_Mix.model')

    # create features spaces (all features)

	
	
    f = open('classify.txt','w+')
    f1 = open('tweet.txt','w+')
    predict = "happy"

    # Start crawling
    ts = crawler.TwitterStream()
    ts.setup_connection()
    ts.start()

    # Get tweets results
    result = ts.get_result()

    html = "<html>" + get_style() + \
           "<body><div id=\"wrapper\">" \
           "CIS630 Project 2 - Twitter Affect" + \
           "<br><strong>Crawling Results:</strong>" + \
           "<table><tr><th>tweets</th><th>Emotion</th></tr>"
    count=1
    if result == []:
        result = ["Not implemented yet"]
    for tweet in result:
        predict = predictEmotion(tweet, fs, model)
        html = html + "<tr><td>" + str(count)+ ' '+tweet + "</td><td>" +predict+"</td><tr>"
	count+=1
	f.write(predict+'\n')


    html = html + "</table><br><a href=\"crawler\">Back</a>" \
                  "</div></body></html>"
    f.close()
    f1.close()
    return HttpResponse(html)


# input: tweet
#{'Test_Happy.txt':1,'Test_Angry.txt':0,'Test_Sad.txt':2,'Test_Ashamed.txt':3,'Test_Afraid.txt':4}

def predictEmotion(tweet, fs, model):
    vectors = []
    vector = Mix_IG.vectorize(fs, tweet)
    vectors.append(vector)
    labels = [0]

    m_happy, p_acc, p_happy = svm_predict(labels, vectors, happy_model, '-b 1')
    m_sad, p_acc, p_sad = svm_predict(labels, vectors, sad_model, '-b 1')
    m_angry, p_acc, p_angry = svm_predict(labels, vectors, angry_model, '-b 1')
    m_ashamed, p_acc, p_ashamed = svm_predict(labels, vectors, ashamed_model, '-b 1')
    m_afraid, p_acc, p_afraid = svm_predict(labels, vectors, afraid_model, '-b 1')
	
    tempZ = []
    tempZ.append(p_angry[0][1])
    tempZ.append(p_happy[0][1])
    tempZ.append(p_sad[0][1])	
    tempZ.append(p_ashamed[0][1])
    tempZ.append(p_afraid[0][0])
	
    print max(tempZ)
	
    if(max(tempZ)<0.6):
    	return "neutral"

    m, p_acc, p_vals = predict(labels, vectors, model)

    map = {1 : "happy", 0 : "angry", 2 : "sad", 3 : "ashamed", 4 : "afraid"}

    return map[m[0]]







# CSS file
def get_style():
    style = "<head><style>" \
            "body {font-family: 'Droid Sans', 'Trebuchet Ms', verdana; font-size: 18px; background-color: #E7F3FF;}" \
            "td, th     {border:2px solid #35BDF5;padding:3px 7px 2px 7px;}" \
            "th       {text-align:center; padding-top:5px; padding-bottom:4px; background-color:#35bdf5; color:#ffffff;}" \
            "tr.alt td    { background-color:#e9f4ff;}" \
            "</style></head>"
    return style
