Last login: Fri Apr 28 09:30:45 on console
wirelessprv-10-193-49-103:~ Ann$ ssh hgong6@golub.campuscluster.illinois.edu
hgong6@golub.campuscluster.illinois.edu's password: 
Last login: Wed Apr 26 11:30:15 2017 from wirelessprv-10-193-49-103.near.illinois.edu
************************************************************************

          Welcome to Campus Cluster @ University of Illinois

                Unauthorized use/access is prohibited

------------------------------------------------------------------------

             This is the login node to the CampusCluster

------------------------------------------------------------------------

  Please send questions or concerns to help@campuscluster.illinois.edu

************************************************************************

User Forum:
    https://campuscluster.illinois.edu/forum/

    The forum is set up for the users and all users are welcome to
    ask questions or contribute knowledge.  Admins will periodically
    read the forums and answer questions posed, if it is appropriate.

User Guide:
    https://campuscluster.illinois.edu/user_info/doc/

Beginner's Guide:
    https://campuscluster.illinois.edu/user_info/doc/beginner.html


** WARNING **  ** WARNING **  ** WARNING **  ** WARNING **  ** WARNING **

Quotas on user home directories will be enforced starting Monday December 9,
2013 at 7 a.m. CT. The soft limit is 2 GB and the hard limit is 4 GB. Once
quotas are enforced, if the amount of data in your home directory is over
the soft limit of 2 GB but under the hard limit of 4 GB, there is a grace
period of 7 days to get under the soft limit. When the grace period expires,
you will not be able to write new files or update any current files until
you reduce the amount of data to below 2 GB.

For those users over the hard limit that also have jobs running out of a
home directory, those jobs are liable to crash.

------------------------------------------------------------------------

As of Friday May 16, 2014 we have implemented a script that will
automatically kill processes on the login nodes that use more than
30 minutes of CPU time or are running on more than 4 processors.

** WARNING **  ** WARNING **  ** WARNING **  ** WARNING **  ** WARNING **

********************************************************************


  
+

Directories quota usage for user hgong6:

-------------------------------------------------------------------------------------
|      Fileset       |  Used   |  Soft   |  Hard   |   Used   |   Soft   |   Hard   |
|                    |  Block  |  Quota  |  Limit  |   File   |   Quota  |   Limit  |
-------------------------------------------------------------------------------------
| home               | 1.535G  | 2G      | 4G      | 26578    | 0        | 0        |
| viswanath          | 1.492T  | 0       | 0       | 1078840  | 9000000  | 12000000 |
-------------------------------------------------------------------------------------

+

[hgong6@golubh1 ~]$ cd /projects/csl/viswanath/data/hgong6/Preposition/
[hgong6@golubh1 Preposition]$ ls  
coarse_prep_sense    preposition_selection         sense_embedding   vpc
data                 semantic_role                 spatial_relation
label_senses_coprus  semantic_role_disambiguation  src
[hgong6@golubh1 Preposition]$ cd ../
[hgong6@golubh1 hgong6]$ ls
Composition_Applications  NLP_Tools                    impact1
Corpus                    PP_ambiguity_data            impact2
Domain_Extraction         Preposition                  software
GITHUB                    SpellingCorrection           spark
GPUData                   WordEmbedding                tData
IBM                       automatic_detection_of_mwes  tmp.txt
LanguageModel             courses                      vectors_test.txt
MWE_extraction            download.py
Main.pbs                  hw
[hgong6@golubh1 hgong6]$ cd Preposition/spatial_relation/
[hgong6@golubh1 spatial_relation]$ ls
Main.pbs       pca.py                      test.txt
dumped_folder  pca.pyc                     train.txt
funcWords.txt  spatial.o5838076            vocab_threeSides.py
logs           spatial_relation.py         vocab_threeSides.pyc
old_vocab.py   spatial_relation_no_log.py
[hgong6@golubh1 spatial_relation]$ vi spatial.o5838076 
[hgong6@golubh1 spatial_relation]$ vi logs/
in_avg_wrong.txt  in_wrong.txt      on_avg_wrong.txt  on_wrong.txt
[hgong6@golubh1 spatial_relation]$ vi logs/in_wrong.txt 
[hgong6@golubh1 spatial_relation]$ vi logs/in_wrong.txt 
[hgong6@golubh1 spatial_relation]$ vi logs/on_wrong.txt 
[hgong6@golubh1 spatial_relation]$ ls 
Main.pbs       pca.py                      test.txt
dumped_folder  pca.pyc                     train.txt
funcWords.txt  spatial.o5838076            vocab_threeSides.py
logs           spatial_relation.py         vocab_threeSides.pyc
old_vocab.py   spatial_relation_no_log.py
[hgong6@golubh1 spatial_relation]$ vi train.txt 
[hgong6@golubh1 spatial_relation]$ vi test.txt 
[hgong6@golubh1 spatial_relation]$ vi spatial
[hgong6@golubh1 spatial_relation]$ vi spatial_relation
[hgong6@golubh1 spatial_relation]$ vi spatial_relation.py 
[hgong6@golubh1 spatial_relation]$ vi test.txt 
[hgong6@golubh1 spatial_relation]$ vi train.txt 
[hgong6@golubh1 spatial_relation]$ vi test.txt 
[hgong6@golubh1 spatial_relation]$ vi train.txt 
[hgong6@golubh1 spatial_relation]$ vi test.txt 
[hgong6@golubh1 spatial_relation]$ wc -l train.txt 
419 train.txt
[hgong6@golubh1 spatial_relation]$ wc -l test.txt 
81 test.txt
[hgong6@golubh1 spatial_relation]$ vi logs/
in_avg_wrong.txt  in_wrong.txt      on_avg_wrong.txt  on_wrong.txt
[hgong6@golubh1 spatial_relation]$ vi logs/in_avg_wrong.txt 
[hgong6@golubh1 spatial_relation]$ vi train.txt 
[hgong6@golubh1 spatial_relation]$ vi train.txt 
[hgong6@golubh1 spatial_relation]$ vi train.txt 
[hgong6@golubh1 spatial_relation]$ vi train.txt 
[hgong6@golubh1 spatial_relation]$ vi test.txt 
[hgong6@golubh1 spatial_relation]$ vi train.txt 
[hgong6@golubh1 spatial_relation]$ vi train.txt 
[hgong6@golubh1 spatial_relation]$ vi train.txt 
[hgong6@golubh1 spatial_relation]$ cd ..
[hgong6@golubh1 Preposition]$ cd ../SpellingCorrection/
[hgong6@golubh1 SpellingCorrection]$ ls
SpellingCorrection  data  src
[hgong6@golubh1 SpellingCorrection]$ cd ..
[hgong6@golubh1 hgong6]$ cd SpellingCorrection/SpellingCorrection/
[hgong6@golubh1 SpellingCorrection]$ ls
Main.pbs     context_based_selection   preprocess
README.md    domain_corpus_generation  result_logs
__init__.py  funcWords.txt             setup.py
add_errors   main.py                   spelling.o5916896
candidates   perspective_evaluation    spelling_correction_evaluation
[hgong6@golubh1 SpellingCorrection]$ cd domain_corpus_generation/
[hgong6@golubh1 domain_corpus_generation]$ ls
Main.pbs        embeddings         perspective_corpus_util.py  tok_train.txt
__init__.py     missing_words.txt  spelling.o5918428           train.txt
corpus_util.py  norm_test.txt      test.txt                    twokenize.py
dict.pickle     norm_train.txt     tok_test.txt                twokenize.pyc
[hgong6@golubh1 domain_corpus_generation]$ vi norm_train.txt 
[hgong6@golubh1 domain_corpus_generation]$ vi train.txt 
[hgong6@golubh1 domain_corpus_generation]$ vi norm_train.txt 
[hgong6@golubh1 domain_corpus_generation]$ cd ..  
[hgong6@golubh1 SpellingCorrection]$ module load git
[hgong6@golubh1 SpellingCorrection]$ git add domain_corpus_generation/norm_train.txt 
[hgong6@golubh1 SpellingCorrection]$ git add domain_corpus_generation/norm_test.txt 
[hgong6@golubh1 SpellingCorrection]$ git commit -m "normalized dataset"
[master d87b672] normalized dataset
 Committer: Gong <hgong6@golubh1.campuscluster.illinois.edu>
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
You can suppress this message by setting them explicitly:

    git config --global user.name "Your Name"
    git config --global user.email you@example.com

After doing this, you may fix the identity used for this commit with:

    git commit --amend --reset-author

 2 files changed, 159686 insertions(+), 0 deletions(-)
 create mode 100644 domain_corpus_generation/norm_test.txt
 create mode 100644 domain_corpus_generation/norm_train.txt
[hgong6@golubh1 SpellingCorrection]$ git push origin master
Username: 
Password: 
error: The requested URL returned error: 403 Forbidden while accessing https://github.com/MUSE-UIUC/SpellingCorrection.git/info/refs

fatal: HTTP request failed
[hgong6@golubh1 SpellingCorrection]$ git push origin master
Username: 
Password: 
To https://github.com/MUSE-UIUC/SpellingCorrection.git
 ! [rejected]        master -> master (non-fast-forward)
error: failed to push some refs to 'https://github.com/MUSE-UIUC/SpellingCorrection.git'
To prevent you from losing history, non-fast-forward updates were rejected
Merge the remote changes (e.g. 'git pull') before pushing again.  See the
'Note about fast-forwards' section of 'git push --help' for details.
[hgong6@golubh1 SpellingCorrection]$ git pull origin master
remote: Counting objects: 171, done.
remote: Compressing objects: 100% (171/171), done.
remote: Total 171 (delta 38), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (171/171), 392.48 KiB, done.
Resolving deltas: 100% (38/38), done.
From https://github.com/MUSE-UIUC/SpellingCorrection
 * branch            master     -> FETCH_HEAD
error: Your local changes to the following files would be overwritten by merge:
	domain_corpus_generation/corpus_util.py
Please, commit your changes or stash them before you can merge.
Aborting
[hgong6@golubh1 SpellingCorrection]$ git push origin master
Username: 
Password: 
To https://github.com/MUSE-UIUC/SpellingCorrection.git
 ! [rejected]        master -> master (non-fast-forward)
error: failed to push some refs to 'https://github.com/MUSE-UIUC/SpellingCorrection.git'
To prevent you from losing history, non-fast-forward updates were rejected
Merge the remote changes (e.g. 'git pull') before pushing again.  See the
'Note about fast-forwards' section of 'git push --help' for details.
[hgong6@golubh1 SpellingCorrection]$ git add domain_corpus_generation/corpus_util.py 
[hgong6@golubh1 SpellingCorrection]$ git push origin master
Username: 
Password: 
To https://github.com/MUSE-UIUC/SpellingCorrection.git
 ! [rejected]        master -> master (non-fast-forward)
error: failed to push some refs to 'https://github.com/MUSE-UIUC/SpellingCorrection.git'
To prevent you from losing history, non-fast-forward updates were rejected
Merge the remote changes (e.g. 'git pull') before pushing again.  See the
'Note about fast-forwards' section of 'git push --help' for details.
[hgong6@golubh1 SpellingCorrection]$ git pull origin master
From https://github.com/MUSE-UIUC/SpellingCorrection
 * branch            master     -> FETCH_HEAD
error: Your local changes to the following files would be overwritten by merge:
	domain_corpus_generation/corpus_util.py
Please, commit your changes or stash them before you can merge.
Aborting
[hgong6@golubh1 SpellingCorrection]$ git add domain_corpus_generation/corpus_util.py 
[hgong6@golubh1 SpellingCorrection]$ git push origin master
Username: 
Password: 
To https://github.com/MUSE-UIUC/SpellingCorrection.git
 ! [rejected]        master -> master (non-fast-forward)
error: failed to push some refs to 'https://github.com/MUSE-UIUC/SpellingCorrection.git'
To prevent you from losing history, non-fast-forward updates were rejected
Merge the remote changes (e.g. 'git pull') before pushing again.  See the
'Note about fast-forwards' section of 'git push --help' for details.
[hgong6@golubh1 SpellingCorrection]$ git status
# On branch master
# Your branch is ahead of 'origin/master' by 1 commit.
#
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#	modified:   domain_corpus_generation/corpus_util.py
#
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#	modified:   main.py
#
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#
#	Main.pbs
#	__init__.py
#	domain_corpus_generation/Main.pbs
#	domain_corpus_generation/__init__.py
#	domain_corpus_generation/embeddings/
#	domain_corpus_generation/missing_words.txt
#	domain_corpus_generation/perspective_corpus_util.py
#	domain_corpus_generation/spelling.o5918428
#	domain_corpus_generation/test.txt
#	domain_corpus_generation/tok_test.txt
#	domain_corpus_generation/tok_train.txt
#	domain_corpus_generation/train.txt
#	domain_corpus_generation/twokenize.py
#	domain_corpus_generation/twokenize.pyc
#	preprocess/
#	result_logs/
#	setup.py
#	spelling.o5916896
[hgong6@golubh1 SpellingCorrection]$ 
[hgong6@golubh1 SpellingCorrection]$                                        
[hgong6@golubh1 SpellingCorrection]$ 
[hgong6@golubh1 SpellingCorrection]$ 
[hgong6@golubh1 SpellingCorrection]$ 
[hgong6@golubh1 SpellingCorrection]$ 
[hgong6@golubh1 SpellingCorrection]$ 
[hgong6@golubh1 SpellingCorrection]$ 
[hgong6@golubh1 SpellingCorrection]$ 
[hgong6@golubh1 SpellingCorrection]$   
[hgong6@golubh1 SpellingCorrection]$ 
[hgong6@golubh1 SpellingCorrection]$ ls        
fdMain.pbs     context_based_selection   preprocess
README.md    domain_corpus_generation  result_logs
__init__.py  funcWords.txt             setup.py
add_errors   main.py                   spelling.o5916896
candidates   perspective_evaluation    spelling_correction_evaluation
[hgong6@golubh1 SpellingCorrection]$    
[hgong6@golubh1 SpellingCorrection]$ 
[hgong6@golubh1 SpellingCorrection]$ 
[hgong6@golubh1 SpellingCorrection]$ 
[hgong6@golubh1 SpellingCorrection]$ 
[hgong6@golubh1 SpellingCorrection]$ ls
Main.pbs     context_based_selection   preprocess
README.md    domain_corpus_generation  result_logs
__init__.py  funcWords.txt             setup.py
add_errors   main.py                   spelling.o5916896
candidates   perspective_evaluation    spelling_correction_evaluation
[hgong6@golubh1 SpellingCorrection]$ ls 
Main.pbs     context_based_selection   preprocess
README.md    domain_corpus_generation  result_logs
__init__.py  funcWords.txt             setup.py
add_errors   main.py                   spelling.o5916896
candidates   perspective_evaluation    spelling_correction_evaluation
[hgong6@golubh1 SpellingCorrection]$ git status
# On branch master
# Your branch is ahead of 'origin/master' by 1 commit.
#
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#	modified:   domain_corpus_generation/corpus_util.py
#
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#	modified:   main.py
#
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#
#	Main.pbs
#	__init__.py
#	domain_corpus_generation/Main.pbs
#	domain_corpus_generation/__init__.py
#	domain_corpus_generation/embeddings/
#	domain_corpus_generation/missing_words.txt
#	domain_corpus_generation/perspective_corpus_util.py
#	domain_corpus_generation/spelling.o5918428
#	domain_corpus_generation/test.txt
#	domain_corpus_generation/tok_test.txt
#	domain_corpus_generation/tok_train.txt
#	domain_corpus_generation/train.txt
#	domain_corpus_generation/twokenize.py
#	domain_corpus_generation/twokenize.pyc
#	preprocess/
#	result_logs/
#	setup.py
#	spelling.o5916896
[hgong6@golubh1 SpellingCorrection]$ git push origin master
Username: 
Password: 
To https://github.com/MUSE-UIUC/SpellingCorrection.git
 ! [rejected]        master -> master (non-fast-forward)
error: failed to push some refs to 'https://github.com/MUSE-UIUC/SpellingCorrection.git'
To prevent you from losing history, non-fast-forward updates were rejected
Merge the remote changes (e.g. 'git pull') before pushing again.  See the
'Note about fast-forwards' section of 'git push --help' for details.
[hgong6@golubh1 SpellingCorrection]$ git pull origin master
From https://github.com/MUSE-UIUC/SpellingCorrection
 * branch            master     -> FETCH_HEAD
error: Your local changes to the following files would be overwritten by merge:
	domain_corpus_generation/corpus_util.py
Please, commit your changes or stash them before you can merge.
Aborting
[hgong6@golubh1 SpellingCorrection]$ git commit -m "corpus_util update"
[master 6d9a90e] corpus_util update
 Committer: Gong <hgong6@golubh1.campuscluster.illinois.edu>
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
You can suppress this message by setting them explicitly:

    git config --global user.name "Your Name"
    git config --global user.email you@example.com

After doing this, you may fix the identity used for this commit with:

    git commit --amend --reset-author

 1 files changed, 27 insertions(+), 5 deletions(-)
[hgong6@golubh1 SpellingCorrection]$ git push origin master
Username: 
Password: 
To https://github.com/MUSE-UIUC/SpellingCorrection.git
 ! [rejected]        master -> master (non-fast-forward)
error: failed to push some refs to 'https://github.com/MUSE-UIUC/SpellingCorrection.git'
To prevent you from losing history, non-fast-forward updates were rejected
Merge the remote changes (e.g. 'git pull') before pushing again.  See the
'Note about fast-forwards' section of 'git push --help' for details.
[hgong6@golubh1 SpellingCorrection]$ vi domain_corpus_generation/corpus_util.py 
 
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









