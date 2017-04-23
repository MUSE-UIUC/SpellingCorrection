"""
context-sensitive spelling correction
"""

import numpy as np
from pca import PCA
from vocab import Vocab
from nltk import word_tokenize

embedding_directory = "/projects/csl/viswanath/data/hgong6/Preposition/data/prepositions_word_vector/"
vocabInputFile = "vocab.txt"
vectorInputFile = "vectors.bin"

def cosSim(array1, array2):
        if (np.linalg.norm(array1) * np.linalg.norm(array2)) == 0:
                return 0
        return np.dot(array1, array2) / (np.linalg.norm(array1) * np.linalg.norm(array2))

    
def pcaSenEmb(sent_vecs, var_threshold = 0.6):
    """
    output: basis of context space
    """
    pca = PCA()
    pca.fit(sent_vecs)
    var_list = pca.explained_variance_ratio_
    cand = 0
    var_sum = 0
    for var in var_list:
        var_sum += var
        cand += 1
        if (var_sum >= var_threshold):
            break
    basis = pca.components_
    return basis

def getRelevance(X, w):
    """
    X: context space
    w: word vector
    """
    X = np.array(X)
    mat = np.dot(X, np.transpose(X))
    w = np.array(w)
    col = np.dot(X,w)
    coef = np.linalg.solve(mat,col)
    w_appro = np.dot(np.transpose(X),coef)
    relevance = cosSim(w,w_appro)
    return relevance

def scoreWord(cand_words,  sent, vecDim, isFunctional):
    """
    input:
    cand_words: a list of legal words
    sent: a list of context words within a context window
    output:
    scores: a list of scores corresponding to each candidate
    """
    vocab = Vocab(vecDim, vocabInputFile, vectorInputFile, isFunctional) # !!
    word_vecs = vocab.getVectors(cand_words)
    sent_vecs = vocab.getVectors(sent)
    if (len(sent_vecs) <= 3):
        sent_vec = np.sum(sent_vecs, axis=0)
        scores = [cosSim(sent_vec, word_vec) for word_vec in word_vecs]
    else:
        sent_space = pcaSenEmb(sent_vecs, var_threshold = 0.6)
        scores=  [getRelevance(sent_space, word_vec) for word_vec in word_vecs]
    best_word = cand_words[np.argmax(scores)]
    return best_word, scores




















    
