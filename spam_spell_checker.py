"""
spelling checker of spam data
"""

from nltk.stem.wordnet import WordNetLemmatizer
from spam.spam_util import lemmatizeText, getFileNames, preprocess
from pyxdameraulevenshtein import damerau_levenshtein_distance as dist
import pickle
from domain_corpus_generation.corpus_util import loadDict
from context_based_selection.vocab import Vocab
#from context_based_selection.pca import PCA
from context_based_selection.context_score import cosSim, pcaSenEmb, getRelevance
import os
import numpy as np


# NEW CORPUS !!!
# NEW embedding
corpus = loadDict(fn="domain_corpus_generation/dict_v1.pickle", freq_threshold=1000)
vecDim = 300
embedding_directory = "/projects/csl/viswanath/data/hgong6/SpellingCorrection/SpellingCorrection/domain_corpus_generation/embeddings/"
vocabInputFile = "spam_vocab.txt"
vectorInputFile = "spam_vectors.bin"
isFunctional = 1
vocab = Vocab(vecDim, embedding_directory, vocabInputFile, vectorInputFile, isFunctional) # !!
CAND_LIMIT = 4

"""
def lemmatizeText(word_list):
    lmtzr = WordNetLemmatizer()
    lemma_word_list = [lmtzr.lemmatize(word) for word in word_list]
    return lemma_word_list
        
def tmp(text):
    #remove non-words
    #input: stop-enabled text (stop/*.txt)
    #output: a list of words without non-words (e.g., numbers and punctuations)
    #             a list of lemmas without non-words               

    # pos tagging
    VERB_TAGS = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    raw_word_list = text.strip().lower().split()
    word_tag_list = nltk.pos_tag(raw_word_list)
    # remove non-words such as numbers and punctuations
    alpha_inds = [ind for ind in range(len(raw_word_list)) if raw_word_list[ind].isalpha()]
    word_tag_list = [word_tag_list[ind] for ind in alpha_inds]
    # lemmatization based on pos tags
    word_list = []
    lemma_list = []
    lmtzr = WordNetLemmatizer()
    for (word, tag) in word_tag_list:
        if (tag in NON_WORD_TAGS):
            continue
        word_list.append(word)
        if (tag in VERB_TAGS):
            lemma = lmtzr.lemmatize(word, "v")
        else:
            lemma = lmtzr.lemmatize(word)
        lemma_list.append(lemma_word)
    return word_list, lemma_list
"""

def getCandFromDict(word):
    """
    input: word
    output: cand_words, freq
    """
    cand_words = []
    freq_list = []
    cur_dist = 0
    while (cand_words == [] and cur_dist <= 3):
        cur_dist += 1
        for key in corpus:
            if (dist(key, word) <= cur_dist):
                cand_words.append(key)
                freq_list.append(corpus[key])
    if (freq_list != []):
        sort_inds = np.argsort(freq_list)[::-1]
        sort_words = [cand_words[ind] for ind in sort_inds]
        sort_freq = [freq_list[ind] for ind in sort_inds]
    else:
        sort_words = cand_words[:]
        sort_freq = [0] * len(cand_words)
    return sort_words, sort_freq


def getContext(sent_seq, word_ind, context_size):
    context_words = []
    word_num = len(sent_seq)
    # left_context
    left_ind = word_ind - 1
    left_num = 0
    while (left_ind >= 0 and left_num <= context_size):
        left_word = sent_seq[left_ind]
        if (left_word in corpus):
            context_words.append(left_word)
            left_num += 1
        left_ind -= 1
    # right context
    right_ind = word_ind + 1
    right_num = 0
    while (right_ind < word_num and right_num <= context_size):
        right_word = sent_seq[right_ind]
        if (right_word in corpus):
            context_words.append(right_word)
            right_num += 1
        right_ind += 1
    return context_words



def scoreCandidates(cand_words, context_words):
    """
    input: a list of words, context sequence
    output: sorted cand words, scores (both in decreasing order)
    """
    word_vecs = vocab.getVectors(cand_words)
    sent_vecs = vocab.getVectors(context_words)
    #print "sent_vecs shape", len(sent_vecs), len(sent_vecs[0])
    if (len(sent_vecs)==0 or len(word_vecs)==0):
        scores = [0] * len(cand_words)
    elif (len(sent_vecs) <= 3):
        #print "avg representation of sentence..."
        sent_vec = np.sum(sent_vecs, axis=0)
        scores = [cosSim(sent_vec, word_vec) for word_vec in word_vecs]
    else:
        #print "pca representation of sentence..."
        sent_space = pcaSenEmb(sent_vecs, var_threshold = 0.5)
        scores=  [getRelevance(sent_space, word_vec) for word_vec in word_vecs]
    sort_ind = np.argsort(scores)[::-1] # largest comes first
    sorted_cand_words = [cand_words[ind] for ind in sort_ind]
    sorted_scores = [scores[ind] for ind in sort_ind]
    return sorted_cand_words, sorted_scores



def correctSent(word_list, context_size):
    """
    input: wrong word_list
    output: revised_word_list, corr, cand_corr
    """
    revised_word_list = word_list[:]
    corr = []
    cand_corr = []
    word_num = len(word_list)
    for ind in range(word_num):
        word = word_list[ind]
        if (word not in corpus):
            cand_words, sort_freq = getCandFromDict(word)
            cand_words = cand_words[:CAND_LIMIT] # limit # of candidates
            context_words = getContext(word_list, ind, context_size)
            sorted_cand_words, sorted_scores = scoreCandidates(cand_words, context_words)
            if (len(sorted_cand_words) > 0):
                revised_word_list[ind] = sorted_cand_words[0]
                corr.append((sorted_cand_words[0], word))
                cand_corr.append(",".join(sorted_cand_words)+" -> "+word)
    return revised_word_list, corr, cand_corr
            

def generateAlgoCorrections(texts, context_size=10):
    """
    input: revised text (not lemma)
    output: corrected_sent_seq, corrected_word_pairs, cand_corrections
    """
    corrected_sent_seq = []
    corrected_word_pairs = []
    cand_corrections = []
    for text in texts:
        word_list = text.strip().lower().split()
        revised_word_list, corr, cand_corr = correctSent(word_list, context_size)
        corrected_sent_seq.append(revised_word_list[:])
        corrected_word_pairs.append(corr[:])
        cand_corrections.append(cand_corr[:])
    return corrected_sent_seq, corrected_word_pairs, cand_corrections


def lemmatizeCorrections(corrected_sent_seq):
    """
    input: corrected text sequence
    output: lemmatized corrected text
    """
    lemma_text_list = []
    for word_list in corrected_sent_seq:
        lemma_list = lemmatizeText(word_list)
        lemma_text = " ".join(lemma_list)
        lemma_text_list.append(lemma_text)
       
    return lemma_text_list


def readRevisedText(revised_folder="spam/spam_data/spam-test-w-errors/"):
    revised_text_list = []
    gold_cor_list = []
    for fn in os.listdir(revised_folder):
	if (not fn.endswith(".txt")):
	    continue
        f = open(revised_folder+fn, "r")
	seq = f.readlines()
	f.close()
	if (len(seq)==2):
	    orig_text, revised_text = seq
	    cor_seq = []
	else:
            orig_text, revised_text, cor_str = seq
            cor_seq = cor_str.strip().split(";") # ["a,b", "c,d"]
	    cor_seq = [s.strip().split(",") for s in cor_seq] # [["a ", "b "], ["c "," d"]]
            cor_seq = [(t[0].strip(), t[1].strip()) for t in cor_seq if len(t)>1] #  [["a", "b"], ["c","d"]]
        revised_text_list.append(revised_text.strip())
        gold_cor_list.append(cor_seq[:])
    return revised_text_list, gold_cor_list


def evalCorrections(gold_corrections, algo_corrections, cand_corrections):
    total_gold_corrections = 0
    total_algo_corrections = 0
    correct_algo_corrections = 0
    # log candidates
    logs = open("spam_wrong_logs.txt", "w")
    for ind in range(len(gold_corrections)):
        gold_list = gold_corrections[ind]
        algo_list = algo_corrections[ind]
        total_gold_corrections += len(gold_list)
        total_algo_corrections += len(algo_list)
        for tup in gold_list:
            if (tup in algo_list):
                correct_algo_corrections += 1
            else:
                print >> logs, str(tup)+"\t"+str(cand_corrections[ind])
    logs.close()
    # prec, recall & fscore
    prec = 1.0 * correct_algo_corrections / total_algo_corrections
    recall = 1.0 * correct_algo_corrections / total_gold_corrections
    fscore = 2 * prec * recall / (prec + recall)
    print "prec %f , recall %f , fscore %f" % (prec, recall, fscore)
    print "total_gold_corrections: %f , correct_algo_corrections: %f" % (total_gold_corrections, correct_algo_corrections)


def writeCorrections(revised_folder="spam/spam_data/spam-test-w-errors/", output_folder="spam/spam_data/corrected-test/"):

    # read revised sent
    revised_text_list, gold_cor_list = readRevisedText(revised_folder)
    
    # algorithmic corrections
    corrected_text_seq, algo_cor_list, cand_corrections = generateAlgoCorrections(revised_text_list)

    # eval correction
    evalCorrections(gold_cor_list, algo_cor_list, cand_corrections)
    
    # lemmatize for spam detection
    lem_corrected_text_list= lemmatizeCorrections(corrected_text_seq)
    fns = os.listdir(revised_folder)
    fns = [fn for fn in fns if fn.endswith(".txt")]
    for ind in range(len(fns)):
        text = lem_corrected_text_list[ind]
        fn = fns[ind]
        g = open(output_folder+fn, "w")
        print >> g, text
        g.close()
    print "done writing lem-corrected-spam data..."
    

if __name__=="__main__":
    """
    file in orig-test -> preprocess -> add error to word based on lemma -> revised word list
    revised file -> spam detection accuracy
    revised file -> generateAlgoCorrections ->  lemmatizeCorrections -> spam detection accuracy    
    """
    # write lem-corrected spam to corrected-test folder
    writeCorrections()













