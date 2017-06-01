"""
spam analysis
"""
import os

def collectWords(log="spam_wrong_logs.txt"):
    f = open(log, "r")
    lines = f.readlines()
    f.close()
    word_list = []
    for line in lines:
        seq = line.strip().split("\t")
        word_pair = seq[0].split(",")
        word = word_pair[0][1:]
        word_list.append(word)
    word_list = list(set(word_list))
    with open("spam_analysis.txt", "wb") as handle:
        pickle.load(word_list, handle)
    print "done analyzing words..."
    print word_list[:10]


def mailStats(test_spam_folder="spam_data/orig-test/"):
    fns = os.listdir(test_spam_folder)
    fns = [fn for fn in fns if "spmsg" in fn]
    print "# of test spams", len(fns)
    mail_len = []
    for fn in fns:
        f = open(test_spam_folder+fn, "r")
        seq = f.read().strip().split()
        mail_len.append(len(seq))
        f.close()
    print "min len", min(mail_len), "max len", max(mail_len), "avg len", sum(mail_len)*1.0/len(mail_len)
    


if __name__=="__main__":
    #collectWords()
    mailStats()
