"""
read lem-data to generate features
"""

import os
import operator
import collections
from sklearn.naive_bayes import MultinomialNB
import pickle
from sklearn.metrics import accuracy_score
import numpy as np

vocab_size = 2500

def countWord(nonspam_train_folder, spam_train_folder, nonspam_test_folder, spam_test_folder):
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


def evaluate(gold_labels, pred_labels):
    acc = accuracy_score(gold_labels, pred_labels)
    print "acc:", acc


def readFolderText(folder):
    texts = []
    for fn in os.listdir(folder):
        f = open(folder+fn, "r")
        text = f.read().strip()
        texts.append(text)
    return texts


if __name__=="__main__":
    
    nonspam_train_folder = "spam_data/nonspam-train/"
    spam_train_folder = "spam_data/spam-train/"
    nonspam_test_folder = "spam_data/nonspam-test/"

    # standard test data (lemma orig data)
    #print "standard test data..."
    #orig_spam_test_folder = "spam_data/spam-test/"

    # revised test data (with error, lemma)
    #print "revised test data with error..."
    #spam_test_folder = "spam_data/revised-test/"

    # corrected test data (without error, lemma)
    print "corrected data..."
    spam_test_folder = "spam_data/corrected-test/"
    
    countWord(nonspam_train_folder, spam_train_folder, nonspam_test_folder, spam_test_folder)
    nonspam_train_texts = readFolderText(nonspam_train_folder)
    spam_train_texts = readFolderText(spam_train_folder)
    train_texts = nonspam_train_texts + spam_train_texts
    train_labels = [0] * len(nonspam_train_texts) + [1] * len(spam_train_texts)
    train(train_texts, train_labels)

    nonspam_test_texts = readFolderText(nonspam_test_folder)
    spam_test_texts = readFolderText(spam_test_folder)
    test_texts = nonspam_test_texts + spam_test_texts
    gold_test_labels = [0] * len(nonspam_test_texts) + [1] * len(spam_test_texts)
    pred_test_labels = test(test_texts)
    evaluate(gold_test_labels, pred_test_labels)
    











