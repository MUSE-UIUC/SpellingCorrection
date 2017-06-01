"""
spell checker
"""
import argparse
import codecs
from context_based_selection.context_score import scoreWord
import os
import difflib
from nltk.corpus import words
from context_based_selection.vocab import Vocab
#from context_based_selection.pca import PCA
from context_based_selection.context_score import cosSim, pcaSenEmb, getRelevance
import numpy as np
from domain_corpus_generation.corpus_util import loadDict
from preprocess.regular_check import rawCheck, rawCheckOnDist
import editdistance
from pyxdameraulevenshtein import damerau_levenshtein_distance as dist

corpus = loadDict(fn="domain_corpus_generation/dict_v1.pickle", freq_threshold=100)
#small_corpus = loadDict(fn="domain_corpus_generation/dict_v1.pickle", freq_threshold=100) # best: 500, 1500, 500, 100, 200
small_corpus = corpus
train_corpus = loadDict(fn="domain_corpus_generation/persective_train_dict.pickle", freq_threshold=5)

#corpus = loadDict(fn="domain_corpus_generation/standard_en.pickle")
#small_corpus = corpus

vecDim = 300
embedding_directory = "/projects/csl/viswanath/data/hgong6/SpellingCorrection/SpellingCorrection/domain_corpus_generation/embeddings/"
vocabInputFile = "vocab.txt"
vectorInputFile = "vectors.bin"
isFunctional = 1
vocab = Vocab(vecDim, embedding_directory, vocabInputFile, vectorInputFile, isFunctional) # !!
CAND_LIMIT = 4 # 8 - if more candiates are generated, this word might be a non-sense word
DIST_LIMIT = 1


def getCandFromDict(word):
    """
    use edit distance to generate candidates
    input: word
    output: sort_words - words sorted in frequency order with edit distance no larger than 3
                sort_freq - sorted frequency
    """
    cand_words = []
    freq_list = []
    cur_dist = 0

    while (cand_words == [] and cur_dist <=3):
	cur_dist += 1
        for key in small_corpus: # smaller corpus
            ##  levenshtein_distance: transposition = 2
            ##        if (editdistance.eval(key, word) <= DIST_LIMIT):
            ##            cand_words.append(key)

            # damerau_levenshtein_distance: transposition = 1
            if (dist(key, word) <= cur_dist):
                cand_words.append(key)
                freq_list.append(train_corpus[key])
	
    # filter words with low frequency
    if (freq_list != [] and max(freq_list)>0):
	cand_words = [cand_words[ind] for ind in range(len(freq_list)) if freq_list[ind] > 0]	
	freq_list = [freq for freq in freq_list if freq > 0]
        # sort words by frequency
        sort_inds = np.argsort(freq_list)[::-1]
        sort_words = [cand_words[ind] for ind in sort_inds]
        sort_freq = [freq_list[ind] for ind in sort_inds]
    else:
	sort_words = cand_words[:]
	sort_freq = [0] * len(cand_words)
    #print "cand_words", cand_words
    return sort_words, sort_freq



def scoreCandidates(cand_words, context_words):
    """
    input: a list of words, context sequence
    output: sorted cand words, scores (both in decreasing order)
    """
    word_vecs = vocab.getVectors(cand_words)
    sent_vecs = vocab.getVectors(context_words)
    #print "sent_vecs shape", len(sent_vecs), len(sent_vecs[0])
    if (len(sent_vecs)==0):
        scores = [0] * len(cand_words)
    elif (len(sent_vecs) <= 3):
        #print "avg representation of sentence..."
        sent_vec = np.sum(sent_vecs, axis=0)
        scores = [cosSim(sent_vec, word_vec) for word_vec in word_vecs]
    else:
        #print "pca representation of sentence..."
        sent_space = pcaSenEmb(sent_vecs, var_threshold = 0.8)
        scores=  [getRelevance(sent_space, word_vec) for word_vec in word_vecs]
    sort_ind = np.argsort(scores)[::-1] # largest comes first
    sorted_cand_words = [cand_words[ind] for ind in sort_ind]
    sorted_scores = [scores[ind] for ind in sort_ind]
    return sorted_cand_words, sorted_scores


def outputCorrectionSent(sent_seq, context_size):
    """
    correct one sentence
    input: sent_seq - a list of words in a sentence
    output: revised_sent_seq  - a list of words in a sentence
                corr - a list of tuples (corrected_word, error_word)
		cand_corr - a list of a list of candidates
    """
    NUMS = "0123456789"
    word_num = len(sent_seq)
    revised_sent_seq = sent_seq[:]
    cand_corr = []
    corr = []
    for ind in range(word_num):
        word = sent_seq[ind]
        if (len(word) > 30):
	    continue
        # ignore digits
        num_flag = False
        for digit in NUMS:
            if (digit in word):
                num_flag = True
                break
        if (num_flag):
            continue
        
        if (word not in corpus):# !!! big corpus
            # generate candidates
            cand_words, sort_freq = getCandFromDict(word)
            if (len(cand_words) > CAND_LIMIT):
                cand_words = cand_words[:4]
                # START: only choose the most frequent one ?
                # filter out some words with low frequency ?
                #continue

            # context-based detection
            context_words = []
            # left context
            left_ind = ind - 1
            left_num = 0
            while (left_ind>=0 and left_num<=context_size):
		#print "left_ind", left_ind
		#print "sent_len", len(sent_seq)
                if (sent_seq[left_ind] in corpus):
                    context_words.append(sent_seq[left_ind])
                    left_num += 1
                left_ind -= 1
            # right context
            right_ind = ind + 1
            right_num = 0
            while (right_ind<word_num and right_num<=context_size):
                if (sent_seq[right_ind] in corpus):
                    context_words.append(sent_seq[right_ind])
                    right_num += 1
                right_ind += 1
            sorted_cand_words, sorted_scores = scoreCandidates(cand_words, context_words)
            if (len(sorted_cand_words) > 0):
                revised_sent_seq[ind]  = sorted_cand_words[0]
                corr.append((sorted_cand_words[0], word))
		cand_corr.append(",".join(sorted_cand_words)+" -> "+word)
    return revised_sent_seq, corr, cand_corr


def generateTrueCandCorrection(orig_sent_list, error_sent_list, correction_list):
    gold_corrections = []
    for ind in range(len(orig_sent_list)):
        orig_sent_seq = orig_sent_list[ind].strip().split()
        error_sent_seq = error_sent_list[ind].strip().split()
	correct_word = correction_list[ind]
        wrong_word = ""
        for word in error_sent_seq:
            if (word not in orig_sent_seq and dist(word, correct_word)<=1):
                wrong_word = word
                break
        #correct_word = correction_list[ind]
        gold_corrections.append([(correct_word, wrong_word)])
    return gold_corrections


def generateAlgoCandCorrection(sent_str_list, context_size=4):
    """
    input: sent_str_list - a list of strings
    output: revised_sent_seq - a list of a list of tokens
                revised_corrections - a list of a list of tuples
    """
    revised_sent_token = []
    revised_corrections = []
    cand_corrections = []
    # stage 1: context-free check
    sent_token_list, corrections = rawCheckOnDist(sent_str_list, corpus, small_corpus) # rawCheck(sent_str_list)

    # stage 2: context-dependent check
    corrections2 = []
    sent_num = len(sent_token_list)
    for sent_ind in range(sent_num):
        sent_seq = sent_token_list[sent_ind]
        revised_sent_seq, corr, cand_corr = outputCorrectionSent(sent_seq, context_size)
        revised_sent_token.append(revised_sent_seq[:])
        revised_corrections.append(corrections[sent_ind][:]+corr[:])
	cand_corrections.append(cand_corr[:])
    return revised_sent_seq, revised_corrections, cand_corrections
    


def readInputSent(error_type):
    """
    read file with added errors: origin sent, score, error sent, score, corrected word
    return a list of strings
    """
    path = "perspective_evaluation/revise_and_test/output/separated_by_revised_type/"+error_type+"/"
    orig_sent_list = []
    error_sent_list = []
    correction_list = []
    for fn in os.listdir(path):
	if (not fn.endswith(".txt")):
	    continue
        f = open(path+fn, "r")
        lines = f.readlines()
        while (len(lines) >= 6):
            # original sent
            orig_sent = lines.pop(0)
            orig_sent_list.append(orig_sent)
            # original score
            orig_score = float(lines.pop(0))
            # revised sent
            error_sent = lines.pop(0)
            error_sent_list.append(error_sent)
            # revised score
            revised_score = float(lines.pop(0))
            # corrections
	    correction_str = lines.pop(0).strip()
	    #print "cor_str", correction_str
            seq = correction_str.split(";")
	    #print "seq", seq
	    seq = [s.strip() for s in seq]
	    #print (s.split(",")[0].strip(), s.split(",")[1].strip())
            corrections = [(s.split(",")[0].strip(), s.split(",")[1].strip()) for s in seq if s!=""]
            correction_list.append(corrections[:])
            # empty line
            lines.pop(0)
        f.close()
    return orig_sent_list, error_sent_list, correction_list


def evalCorrections(gold_corrections, algo_corrections, cand_corrections, error_type):
    # accuracy: correct_algo_corrections/gold_corrections
    # precision: correct_algo_corrections/total_algo_corrections
    # recall: correction
    total_gold_corrections = 0
    total_algo_corrections = 0
    correct_algo_corrections = 0
    logs = open("logs_"+error_type+".txt", "a+")
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
    prec = 1.0 * correct_algo_corrections / total_algo_corrections
    recall = 1.0 * correct_algo_corrections / total_gold_corrections
    fscore = 2 * prec * recall / (prec + recall)
    print "prec %f , recall %f , fscore %f" % (prec, recall, fscore)
    print "total_gold_corrections: %f , correct_algo_corrections: %f" % (total_gold_corrections, correct_algo_corrections)



if __name__=="__main__":
    error_type_list = ["add", "delete", "permute", "replace", "separate"]
    parser = argparse.ArgumentParser()
    parser.add_argument('--errorType', default="add", type=str)
    args = parser.parse_args()
    error_type = args.errorType

    # read raw data & gold corrections
    #orig_sent_list, error_sent_list, correct_word_list = readInputSent(error_type)
    orig_sent_list, error_sent_list, gold_corrections = readInputSent(error_type)
    # generate gold corrections
    # gold_corrections = generateTrueCandCorrection(orig_sent_list, error_sent_list, correct_word_list)
    
    # generate algo corrections
    revised_sent_seq, algo_corrections, cand_corrections = generateAlgoCandCorrection(error_sent_list)
    # output algo sentences
    # ???
    # evaluate
    evalCorrections(gold_corrections, algo_corrections, cand_corrections, error_type)

    

