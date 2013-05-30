"""
This provides all basic functions for classifier
"""

import re

""" Please modify the root below """
#-----------------------------------------------------------------------
root = "/Users/Alantyy/Dropbox/TwitterAffect"

train_root = root + "/Data/Training"
test_root = root + "/Data/Testing"
#-----------------------------------------------------------------------

# five emotions
emotions = ['happy', 'sad', 'ashamed', 'angry', 'afraid']


def getStopWords():
    """stop words like and, is @, #"""
    stopWords = []
    for word in open(root + "/stoplist.txt").read().split("\n"):
        stopWords.append(word)
    stopWords.append("@")
    stopWords.append("#")
    stopWords.append("[")
    stopWords.append("]")
    return stopWords


def reduceMoreChar(str):
    """happppppy -> happy"""
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", str)


def getAllTweets(emotion):
    """from emotion: afraid, happy, sad, angry, or ashamed"""
    tweets = open(train_root + "/Training_" + emotion + ".txt", 'r').read()
    return tweets



def getOneUnigrams(tweet):
    """ input:    AT_USER i heard about that contest! congrats girl!! """
    """ output:  ['heard', 'congrats'] """
    unigrams = []
    for w in tweet.split():
        print w
        if w in getStopWords():
            continue
        notDigit = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        if notDigit:
            unigrams.append(w)
    return unigrams



def getOneFeatures(tweet):
    """ input:    AT_USER i heard about that contest! congrats girl!! """
    """ output:  ['heard', 'congrats'] """
    return getOneUnigrams(tweet)
    ### use bigram later ####


def generateAllFeatures():
    allFeatures = []
    for emo in emotions:
        tweets = getAllTweets(emo)
        for tweet in tweets[1:3]:
            # e.g. (['hey', 'cici', 'luv', 'mixtape', 'drop', 'soon', 'fantasy', 'ride'], 'positive')
            allFeatures.append((getOneFeatures(tweet), emo))
        for tweet in tweets:
            print getOneFeatures(tweet)

#---------------------- Vectorize --------------------------------------

def vectorize(tweet):
    """ tweet -> {arm: 1, articles: 0, awfully: 0 ...} """
    # read feature list
    allFeatures = open("allFeatures.txt").read().split()
    words = set(tweet)
    # convert tweet into vector
    featureVector = {}
    for feature in allFeatures:
        featureVector[feature] = feature in words
    return featureVector



def getTrainingData():
    priorFeatures = []
    for emo in emotions:
        tweets = getAllTweets(emo)
        for tweet in tweets:
            # e.g. (['hey', 'cici', 'luv', 'mixtape', 'drop', 'soon', 'fantasy', 'ride'], 'positive')
            priorFeatures.append((getOneFeatures(tweet), emo))

    # vectorize all features using nltk batch processing
    trainingData = nltk.classify.util.apply_features(vectorize, priorFeatures)
    return features


#---------------------- Test & Run -----------------------------------

generateAllFeatures()

def main():
    print hello

if "__name__" == "__main__":
    main()
