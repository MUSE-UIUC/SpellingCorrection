"""
feature generation for 
"""
import os
import operator
import collections
from sklearn.naive_bayes import MultinomialNB
import pickle
from sklearn.metrics import accuracy_score
import numpy as np

vocab_size = 2500
def countWord():
    nonspam_train_folder  = "../spam_data/nonspam-train/"
    spam_train_folder = "../spam_data/spam-train/"
    nonspam_test_folder = "../spam_data/nonspam-test/"
    spam_test_folder = "../spam_data/spam-test/"
    word_list = []
    fn_list = [nonspam_train_folder+fn for fn in os.listdir(nonspam_train_folder)] +\
              [spam_train_folder+fn for fn in os.listdir(spam_train_folder)] +\
              [nonspam_test_folder+fn for fn in os.listdir(nonspam_test_folder)] +\
              [spam_test_folder+fn for fn in os.listdir(spam_test_folder)]
    for fn in fn_list:
        f = open(fn, "r")
        text = f.read()
        f.close()
        seq = text.split()
        seq = [word for word in seq if word != "s"]
        word_list.extend(seq)
    counter = collections.Counter(word_list)
    vocab_freq_list = counter.most_common(vocab_size)
    vocab_list = [word_freq[0] for word_freq in vocab_freq_list]

    print "top words", counter.most_common(5)
    with open("vocab.pickle", "wb") as handle:
        pickle.dump(vocab_list, handle)
    print "dumping vocab"

def readFileData(nonspam_folder, spam_folder):
    texts = []
    labels = []
    fn_list = [nonspam_folder+fn for fn in os.listdir(nonspam_folder)] +\
              [spam_folder+fn for fn in os.listdir(spam_folder)]
    labels = [0] * len(os.listdir(nonspam_folder)) + \
             [1] * len(os.listdir(spam_folder))
    for fn in fn_list:
        f = open(fn, "r")
        texts.append(f.read().strip())
    return texts, labels

def train(texts, labels):
    features = []
    with open("vocab.pickle", "rb") as handle:
        vocab_list = pickle.load(handle)
    for doc in texts:
        counter = collections.Counter(doc.strip().split())
        feature = [counter[word] for word in vocab_list]
        features.append(feature)
    clf = MultinomialNB()
    clf.fit(features, labels)
    with open("nbClassifier.pickle", "wb") as handle:
        pickle.dump(clf, handle)
    print "finish dumping model"    

def test(texts):
    """
    texts: a list of strings
    """
    features = []
    with open("vocab.pickle", "rb") as handle:
        vocab_list = pickle.load(handle)
    for doc in texts:
        counter = collections.Counter(doc.strip().split())
        feature = [counter[word] for word in vocab_list]
        features.append(feature)
        
    with open("nbClassifier.pickle", "rb") as handle:
        clf = pickle.load(handle)
    pred_labels = clf.predict(features)
    return pred_labels


def selectToxicWords(topn=100):
    with open("vocab.pickle", "rb") as handle:
        vocab_list = pickle.load(handle)
    with open("nbClassifier.pickle", "rb") as handle:
        clf = pickle.load(handle)
    prob_param = clf.feature_log_prob_
    prob = prob_param[1]-prob_param[0]
    print prob[:5], len(prob)
    sorted_ind = np.argsort(prob)
    sorted_ind = sorted_ind[::-1]
    toxic_words = [vocab_list[ind] for ind in sorted_ind[:]] # smaller the weight, more toxic the word
    with open("toxic_words.pickle", "wb") as handle:
        pickle.dump(toxic_words, handle)
    print "toxic words", toxic_words[:100]


def evaluate(gold_labels, pred_labels):
    acc = accuracy_score(gold_labels, pred_labels)
    print "acc:", acc

if __name__=="__main__":

    """
    # dump vocab
    countWord()

    # train data
    nonspam_train_folder  = "../spam_data/nonspam-train/"
    spam_train_folder = "../spam_data/spam-train/"
    train_texts, train_labels = readFileData(nonspam_train_folder, spam_train_folder)
    train(train_texts, train_labels)
    
    # original test data
    nonspam_test_folder = "../spam_data/nonspam-test/"
    spam_test_folder = "../spam_data/spam-test/"
    test_texts, test_labels = readFileData(nonspam_test_folder, spam_test_folder)
    pred_labels = test(test_texts)
    evaluate(test_labels, pred_labels)
    """

    selectToxicWords()
    
    


