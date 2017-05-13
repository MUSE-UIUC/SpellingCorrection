"""
collect domain-specific data
"""
data_path = "/projects/csl/viswanath/data/hgong6/SpellingCorrection/SpellingCorrection/perspective_evaluation/sentence_toxic_tsv/data/toxicity_annotated_comments.tsv"

def splitTrainTestSent(fn=data_path, saved_train_path="train.txt", saved_test_path="test.txt"):
    f = open(fn, "r")
    lines = f.readlines()
    name = lines.pop(0)
    train_sents = []
    test_sents = []
    train_file = open(saved_train_path, "w")
    test_file = open(saved_test_path, "w")
    for line in lines:
        seq = line.strip().split('\t')
        sent = seq[1]
        sent = sent.replace("NEWLINE_TOKEN", " ")
        sent_type = seq[-1]
        if (sent_type == "train"):
            print >> train_file, sent
        else:
            print >> test_file, sent
    train_file.close()
    test_file.close()
    print "done writing training and test corpus"
    f.close()

if __name__=="__main__":
     splitTrainTestSent()
