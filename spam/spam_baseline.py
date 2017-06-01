"""
spam baseline
revised data -> lemmatization based on 
"""
import os
from spam_util import lemmatizeText

def lemmatizeRevisedText(revised_folder="spam_data/spam-test-w-errors/", output_folder="spam_data/revised-test/"):
    """
    input: text with error added
    output: text 
    """
    revised_text_seq = []
    lemma_texts = []
    fns = os.listdir(revised_folder)
    fns = [fn for fn in fns if fn.endswith(".txt")]
    for fn in fns:
	if (not fn.endswith(".txt")):
	    continue
        f = open(revised_folder+fn, "r")
	seq = f.readlines()
	#print fn, len(seq), seq
        if (len(seq)==2):
	    orig_text, revised_text = seq
	else:
	    #print seq
            orig_text, revised_text, cor_str = seq
        f.close()
        revised_text_seq.append(revised_text.strip().split())
    for word_list in revised_text_seq:
        lemma_list = lemmatizeText(word_list)
        lemma_texts.append(" ".join(lemma_list))
        
    for ind in range(len(fns)):
        g = open(output_folder+fns[ind], "w")
        print >> g, lemma_texts[ind]
        g.close()
    print "done writing revised-test"

if __name__=="__main__":
    lemmatizeRevisedText()
    
