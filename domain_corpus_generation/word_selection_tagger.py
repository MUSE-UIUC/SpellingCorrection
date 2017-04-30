"""
read POS tag from CMU Tweet tagger
"""

TARGET_TAG_SET = ["V", "N", "A"]

def readTag(fn):
    """
    input: fn - pos-tagged file
    output: a list of a list of inds, a list of a list of words
    """
    f = open(fn, "r")
    lines = f.readlines()
    selected_inds = []
    selected_words = []
    tok_sent = []
    for line in lines:
        sent, tag, score, orig_sent = line.strip().split("\t")
        tag_seq = tag.split()
        sent_seq = sent.split()
        inds = [ind for ind in range(len(tag_seq)) if tag_seq[ind] in TARGET_TAG_SET]
        selected_inds.append(inds[:])
        words = [sent_seq[ind] for ind in inds]
        selected_words.append(words[:])
	tok_sent.append(sent)
	#if (len(selected_words)>=2):
	#    break
    return selected_inds, selected_words, tok_sent

if __name__=="__main__":
    selected_inds, selected_words = readTag("tagged_test.txt")
    print selected_inds
    print selected_words
