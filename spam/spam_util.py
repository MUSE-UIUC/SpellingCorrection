"""
utility functions for spam data
"""

from nltk.stem.wordnet import WordNetLemmatizer
import os
import nltk

def getFileNames(lem_data_folder="spam_data/lem-test/"):
    # 1: spam, 0: non-spam
    fns = os.listdir(lem_data_folder)
    print "# of test files", len(fns)
    return fns


def chooseOrigText(lem_data_folder="spam_data/lem-test/", orig_data_folder="spam_data/lingspam_public/stop/", fast_folder="spam_data/orig-test/"):
    fns = getFileNames(lem_data_folder)
    subfolders = os.listdir(orig_data_folder) # ["part1"]
    subfolders = [folder for folder in subfolders if "part" in folder]
    for fn in fns:
        for subfolder in subfolders:
            orig_fns = os.listdir(orig_data_folder+subfolder+"/")
            if (fn in orig_fns):
                os.system("cp "+orig_data_folder+subfolder+"/"+fn+" "+fast_folder)
    print "# of copied files", len(os.listdir(fast_folder))
    print "finish copying original files to", fast_folder
    

def lemmatizeText(word_list):
    """
    input: string text
    output: word list, lemma list
    TO DO: be is not removed
    """
    # pos tagging
    VERB_TAGS = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    word_tag_list = nltk.pos_tag(word_list)

    # lemmatization based on pos tags
    lemma_list = []
    lmtzr = WordNetLemmatizer()
    for (word, tag) in word_tag_list:
        if (tag in VERB_TAGS):
            lemma = lmtzr.lemmatize(word, "v")
        else:
            lemma = lmtzr.lemmatize(word)
        lemma_list.append(lemma)
    return lemma_list    


def preprocess(text): # text: file in stop/
    """
    preprocess the text in folder stop/ by remove non-words
    return: word_list without non-words
    """
    raw_word_list = text.strip().lower().split()
    # remove subject
    if ("subject" in raw_word_list[0]):
        raw_word_list.pop(0)
    # remove non-words such as numbers and punctuations
    alpha_inds = [ind for ind in range(len(raw_word_list)) if raw_word_list[ind].isalpha()]
    word_list = [raw_word_list[ind] for ind in alpha_inds]
    lemma_list = lemmatizeText(word_list)
    return word_list, lemma_list

if __name__=="__main__":
    chooseOrigText()
