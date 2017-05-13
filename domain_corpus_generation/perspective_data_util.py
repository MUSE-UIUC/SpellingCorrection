"""
"""

def splitData(data_folder="/projects/csl/viswanath/data/hgong6/SpellingCorrection/SpellingCorrection/perspective_evaluation/sentence_toxic_tsv/"):
    """
    split data into (train, test) and (toxic, healthy)
    """
    toxicity_dict = dict() # {rev_id: toxicity}
    comment_dict = dict()
    train_toxic_data = []
    train_healthy_data = []
    test_toxic_data = []
    test_healthy_data = []
    
    # annotations
    ant_fn = data_folder+"toxicity_annotations.tsv"
    # comments
    comment_fn = data_folder+"toxicity_annotated_comments.tsv"

    # read multiple annotations
    f = open(ant_fn, "r")
    lines = f.readlines()
    f.close()
    lines.pop(0)
    ant_dict = dict()
    for line in lines:
        rev_id, worker_id, toxicity, score = line.strip().split()
        toxicity = int(toxicity) # 1: toxix, 0: healthy
        if (rev_id not in ant_dict):
            ant_dict[rev_id] = []
        ant_dict[rev_id].append(toxicity)
    # majority votes of toxicity
    for rev_id in ant_dict:
        avg_score = sum(ant_dict[rev_id])
        if (avg_score >= len(ant_dict[rev_id])/2.0):
            toxicity_dict[rev_id] = 1
        else:
            toxicity_dict[rev_id] = 0

    # read comments
    g = open(comment_fn, "r")
    lines = g.readlines()
    g.close()
    lines.pop(0)
    for line in lines:
        seq = line.strip().split()
        rev_id = seq[0]
        comment = seq[1].strip().lower() # ?preprocess?
        sp = seq[-1] # split: train, dev, test
        if (sp == "train" or sp == "dev"):
            if (toxicity_dict[rev_id]==1):
                train_toxic_data.append(comment)
            else:
                train_healthy_data.append(comment)
        if (sp == "test"):
            if (toxicity_dict[rev_id] == 1):
                test_toxic_data.append(comment)
            else:
                test_healthy_data.append(comment)

    # write to files
    fn = "train_toxic_data.txt"
    writeData(fn, train_toxic_data)
    fn = "train_healthy_data.txt"
    writeData(fn, train_healthy_data)
    fn = "test_toxic_data.txt"
    writeData(fn, test_toxic_data)
    fn = "test_healthy_data.txt"
    writeData(fn, test_healthy_data)
        
        
def writeData(fn, comment_list):
    f = open(fn, "w")
    for comment in comment_list:
        print >> fn, comment
    f.close()
    print "finish writing ", fn
    

if __name__=="__main__":
    splitData()
    
    
    
