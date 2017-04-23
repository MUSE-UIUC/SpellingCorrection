import codecs
from context_based_selection.context_score import scoreWord
import os
import difflib
from nltk.corpus import words
from context_based_selection.vocab import Vocab
#from context_based_selection.pca import PCA
from context_based_selection.context_score import cosSim, pcaSenEmb, getRelevance
import numpy as np

corpus = words.words()
vecDim = 300
embedding_directory = "/projects/csl/viswanath/data/hgong6/Preposition/data/prepositions_word_vector/"
vocabInputFile = "vocab.txt"
vectorInputFile = "vectors.bin"
isFunctional = 1
vocab = Vocab(vecDim, embedding_directory, vocabInputFile, vectorInputFile, isFunctional) # !!


def generateGoldCorrection(orig_seq, revised_seq):
    """
    not consider space-separation-error
    """
    gold_orig_revised_list = []
    #print "orig_seq", orig_seq
    #print "revised_seq", revised_seq
    for ind in range(len(orig_seq)):
        orig_word = orig_seq[ind]
        revised_word = revised_seq[ind]
        if (orig_word != revised_word):
            gold_orig_revised_list.append((orig_word, revised_word))
    print "gold_orig_revised_list", gold_orig_revised_list
    return gold_orig_revised_list

def generateBaseCandCorrection(sent_seq):
    orig_revised_list = []
    for word in sent_seq:
        if (word not in corpus):
            cand_word = difflib.get_close_matches(word, corpus, n=1, cutoff=0.1)
            #print "cand_word", cand_word
	    orig_revised_list.append((" ".join(cand_word), word))
    print "base_orig_revised_list", orig_revised_list
    return orig_revised_list

def generateWordCandidates(word):
    cand_words = difflib.get_close_matches(word, corpus, n=6, cutoff=0.5)
    return cand_words

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
	print "avg representation of sentence..."
        sent_vec = np.sum(sent_vecs, axis=0)
        scores = [cosSim(sent_vec, word_vec) for word_vec in word_vecs]
    else:
	print "pca representation of sentence..."
        sent_space = pcaSenEmb(sent_vecs, var_threshold = 0.6)
        scores=  [getRelevance(sent_space, word_vec) for word_vec in word_vecs]
    sort_ind = np.argsort(scores)[::-1] # largest comes first
    sorted_cand_words = [cand_words[ind] for ind in sort_ind]
    sorted_scores = [scores[ind] for ind in sort_ind]
    return sorted_cand_words, sorted_scores


def generateAlgoCandCorrection(sent_seq, context_size=4):
    correct_wrong_list = []
    for ind in range(len(sent_seq)):
        word = sent_seq[ind]
        # illegal word
        if (word not in corpus):
            # find its context -- may add context correction to make it more robust
            context_words = []
            left_ind = ind - 1
            left_num = 0
            while (left_ind >=0 and left_num <= context_size):
                if (sent_seq[left_ind] in corpus):
                    context_words.append(sent_seq[left_ind])
                    left_num += 1
                left_ind -= 1                   
            right_ind = ind + 1
            right_num = 0 
            while (right_ind < len(sent_seq) and right_num <= context_size):
                if (sent_seq[right_ind] in corpus):
                    context_words.append(sent_seq[right_ind])
                    right_num += 1
                right_ind += 1
            # generate candidates
            cand_words = generateWordCandidates(word)
            # score the word in context
            sorted_cand_words, sorted_scores = scoreCandidates(cand_words, context_words)
            # choose the best one in semantics
	    if (len(sorted_cand_words) > 0):
                correct_wrong_list.append((sorted_cand_words[0], word))
    return correct_wrong_list
                

def evalCorrection(gold_dataset, algo_dataset):
    total_corrections = 0
    suggest_corrections = 0
    correct_suggest_corrections = 0
    for ind in range(len(gold_dataset)):
        gold_list = gold_dataset[ind]
        algo_list = algo_dataset[ind]
        total_corrections += len(gold_list)
        suggest_corrections += len(algo_list)
        for tup in gold_list:
            if (tup in algo_list):
                correct_suggest_corrections += 1
    print "total_corrections: %f , suggest_corrections: %f , correct_suggest_corrections: %f" % (total_corrections, suggest_corrections, correct_suggest_corrections)
    prec = 1.0 * correct_suggest_corrections / suggest_corrections
    recall = 1.0 * correct_suggest_corrections / total_corrections
    fscore = 2 * prec * recall / (prec + recall)
    print "prec %f , recall %f , fscore %f" % (prec, recall, fscore)


def readOriginAndRevisedSent(folder):
    """
    return [[(correct word, wrong word), ...]]
    note: allowing multiple wrong words in a sentence
    """
    gold_orig_revised_dataset = []
    base_orig_revised_dataset = []
    algo_orig_revised_dataset = []
    for fn in os.listdir(folder):
        print "fn:", fn
        with codecs.open(folder+fn, 'r', encoding='utf8') as f:
            lines = f.readlines()
            while (len(lines) >= 1):
		tup = []
                for i in range(5):
                    tup.append(lines.pop(0))
		lines.pop(0)
                rev_id, orig_sent, orig_score, revised_sent, revised_score = tup
                orig_seq = orig_sent.lower().strip().split()
                revised_seq = revised_sent.lower().strip().split()
                # gold corrections
                gold_orig_revised_dataset.append(generateGoldCorrection(orig_seq, revised_seq))
                # base corrections
                #base_orig_revised_dataset.append(generateBaseCandCorrection(revised_seq))
                # algo corrections
		algo_orig_revised_dataset.append(generateAlgoCandCorrection(revised_seq))
        break
    # evaluation of methods
    #print "base method"
    #aevalCorrection(gold_orig_revised_dataset, base_orig_revised_dataset)
    print "algo method"
    evalCorrection(gold_orig_revised_dataset, algo_orig_revised_dataset)
                


if __name__=="__main__":
    directory = "/projects/csl/viswanath/data/hgong6/SpellingCorrection/SpellingCorrection/perspective_evaluation/revise_and_test/output/separated_by_revised_type/"
    error_type = ["add", "delete", "permute", "replace"]
    for err in error_type:
        folder = directory+err+"/"
        readOriginAndRevisedSent(folder)


