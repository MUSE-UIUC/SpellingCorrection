"""
regular check using LCS with high threshold
based on a dictionary of frequent words
"""
from domain_corpus_generation.corpus_util import loadDict
import difflib
from pyxdameraulevenshtein import damerau_levenshtein_distance as dist

CONF_THRESHOLD = 0.8
FREQ_THRESHOLD = 500
DICT_PATH = "/projects/csl/viswanath/data/hgong6/SpellingCorrection/SpellingCorrection/domain_corpus_generation/dict_v1.pickle"

# load coprus: a dictionary (word, count)
#raw_corpus = loadDict(DICT_PATH, 10)
#refined_corpus = loadDict(DICT_PATH, FREQ_THRESHOLD)

def rawCheck(sent_list, raw_corpus, refined_corpus):
    """
    scan the sentence to give most confident corrections
    goal: provide as much context as possible

    input: sent_list: a list of string sentences
    output: sent_token_list = [["it", "is", "sunn", "tday"], ["good", "moning"]]
    raw_corrections = [[("sunny", "sunn"), ("today", "tday")], [("morning", "moning")]]
    """
    sent_token_list = []
    raw_corrections = []
    log_file = "/projects/csl/viswanath/data/hgong6/SpellingCorrection/SpellingCorrection/result_logs/raw_check.txt"
    f = open(log_file, "w")
    for sent in sent_list:
        token_list = sent.strip().split()
        corrected_token_list = token_list[:]
        corrections = []
        for ind in range(len(token_list)):
            token = token_list[ind]
            # spelling error
            if (token not in raw_corpus):
		no_raw_check =  True
		"""
                cand_list = difflib.get_close_matches(token, refined_corpus, n=1, cutoff=CONF_THRESHOLD)
                if (cand_list != []):
                    cand_token = cand_list[0]
                    corrected_token_list[ind] = cand_token
                    corrections.append((cand_token, token))
		"""
        sent_token_list.append(corrected_token_list[:])
        raw_corrections.append(corrections[:])
        print >> f, str(corrections)
    f.close()
    print "done stage 1: raw check"
    return sent_token_list, raw_corrections

def getCandFromDict(word, raw_corpus, refined_corpus):
    """
    use edit distance to generate candidates
    input: word
    output: a list of candidate words
    """
    cand_words = []
    cur_dist = 0
    while (cand_words == []):
        cur_dist += 1
        for key in refined_corpus: # smaller corpus
            if (dist(key, word) <= cur_dist):
                cand_words.append(key)
    #print "cand_words", cand_words
    return cand_words



def rawCheckOnDist(sent_list, raw_corpus, refined_corpus):
    """
    similar to rawCheck, but based on edit distance
    """
    sent_token_list = []
    raw_corrections = []
    log_file = "/projects/csl/viswanath/data/hgong6/SpellingCorrection/SpellingCorrection/result_logs/raw_check_editdist.txt"
    f = open(log_file, "w")
    for sent in sent_list:
        token_list = sent.strip().split()
        corrected_token_list = token_list[:]
        corrections = []
        for ind in range(len(token_list)):
            token = token_list[ind]
            # spelling error
            if (token not in raw_corpus):
                cand_list = getCandFromDict(token)
                if (len(cand_list) == 1):
                    cand_token = cand_list[0]
                    corrected_token_list[ind] = cand_token
                    corrections.append((cand_token, token))
        sent_token_list.append(corrected_token_list[:])
        raw_corrections.append(corrections[:])
        print >> f, str(corrections)
    f.close()
    print "done stage 1: raw check on edit distance"
    return sent_token_list, raw_corrections   

if __name__=="__main__":
    print "raw check"
    

    
    
