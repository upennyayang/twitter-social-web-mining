root = "/Users/Alantyy/Dropbox/TwitterAffect"
train_root = root + "/Data/Training"
test_root = root + "/Data/Testing"



def get_stop_words():
    """stop words like and, is @, #"""
    stop_words = []
    for word in open(root + "/stoplist.txt").read().split("\n"):
        stop_words.append(word)
    stop_words.append("@")
    stop_words.append("#")
    stop_words.append("[")
    stop_words.append("]")
    return stop_words


def get_tweets(emotion):
    """ get all tweets for one emotion (afraid, happy, sad, angry, or ashamed) """
    tweets = open(train_root + "/Training_" + emotion + ".txt", 'r').read()
    return tweets

def get_unigram(emotion):


def get_training_set():
    emotions = ['happy', 'sad', 'ashamed', 'angry', 'afraid']
    for emo in emotions:
        tweets = get_tweets(emo)
        for tweet in tweets:
            feature.append((get_unigram(tweet), emo));

    for tweet in all_tweets.split('\n'):



def main():
    # print get_tweets("happy")
    train()

if __name__ == "__main__":
    main()

