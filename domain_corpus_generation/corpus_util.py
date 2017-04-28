"""
construct dictionary
"""
from nltk import word_tokenize
from collections import Counter
import pickle
from twokenize import tokenize


def readWikiVocab(fn="/projects/csl/viswanath/data/hgong6/Preposition/data/prepositions_word_vector/vocab.txt"):
    f = open(fn, "r")
    lines = f.readlines()
    f.close()
    cnt = Counter()
    for line in lines:
        word, freq = line.strip().split()
        cnt[word] += int(freq)
    return cnt

    
def pythonTokenizeText(fn, output_fn):
    f = open(fn, "r")
    lines = f.readlines()
    f.close()
    tok_lines = []
    for line in lines:
        tok_seq = word_tokenize(line.strip().lower().decode('utf8'))
        tok_line = " ".join(tok_seq)
        tok_lines.append(tok_line)
    g = open(output_fn, "w")
    tok_text = "\n".join(tok_lines)
    print >> g, tok_text.encode("utf8")
    print "done processing train text..."


def twitterTokenizeText(fn, output_fn):
    f = open(fn, "r")
    lines = f.readlines()
    f.close()
    tok_lines = []
    for line in lines:
        line = line.strip().lower().decode('utf8')
	line = line.replace("`"," ")
        tok_seq = tokenize(line)
	tok_line = " ".join(tok_seq)
	#print "tok_line", tok_line
	#break
        tok_lines.append(tok_line)
    g = open(output_fn, "w")
    tok_text = "\n".join(tok_lines)
    print >> g, tok_text.encode('utf8')
    print "done twitter tokenizing text...."
        
    
def dumpDict(fn="tok_train.txt"):
    """
    dict: words in lower case
    """
    # word from wikipedia
    cnt = readWikiVocab()
    
    # word from perspective data
    f = open(fn, "r")
    text = f.read()
    f.close()
    text_seq = text.split()
    for word in text_seq:
        cnt[word] += 1

    # dump dictionary
    with open("dict.pickle", "wb") as handle:
        pickle.dump(cnt, handle)
    print "done dumping the vocabulary..."



def loadDict(fn="dict.pickle", freq_threshold=6):
    with open(fn, "rb") as handle:
        cnt = pickle.load(handle)
    rare_words = [word for word in cnt if cnt[word] < freq_threshold]
    for word in rare_words:
        cnt.pop(word)
    print "done loading dictionary..."
    return cnt


def sanityCheck(cnt_dump="dict.pickle", test_fn="tok_test.txt"):
    cnt = loadDict(cnt_dump)

    f = open(test_fn, "r")
    text = f.read()
    text_seq = text.split()
    f.close()

    g = open("missing_words.txt", "w")
    for word in text_seq:
        if (word not in cnt):
            print >> g, word
    g.close()

    print "done sanity check..."

if __name__=="__main__":
    # tokenize train and test data
    #pythonTokenizeText("train.txt", "tok_train.txt")
    #pythonTokenizeText("test.txt", "tok_test.txt")
    twitterTokenizeText("train.txt", "norm_train.txt")
    twitterTokenizeText("test.txt", "norm_test.txt")
    

    # load dictionary
    #dumpDict("tok_train.txt")
    #sanityCheck()






    
    
