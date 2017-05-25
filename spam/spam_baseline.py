"""
spam baseline
revised data -> lemmatization based on 
"""
import os

def lemmatizeRevisedText(revised_folder="spam_data/spam-test-w-errors/", output_folder="spam_data/revised-test/"):
    """
    input: text with error added
    output: text 
    """
    revised_text_seq = []
    lemma_texts = []
    fns = os.listdir(revised_folder)
    for fn in fns:
        f = open(revised_folder+fn, "r")
        orig_text, revised_text, cor_str = f.readlines()
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
    
