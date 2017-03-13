#Project ALDA
#@ Alice Mee Seon Chung

import nltk
import sqlite3
import re
import json
from nltk import *
from nltk.tag import *
from nltk.corpus import stopwords
from nltk.sentiment import *
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment.util import *


def find_insid():
	'''
	find unique instructor id in sql db.
	'''
    db = sqlite3.connect('ins_comment.db')
    c = db.cursor()
    query = 'Select distinct instructor_id from ins_comments;'
    r = c.execute(query)
    resultsls = r.fetchall()
    insid=[]
    for i in range(len(resultsls)):
        insid.append(resultsls[i][0])
    return insid

def find_comments(insid):
	'''
	find all comments by specific instructor id.
	'''
    db = sqlite3.connect('ins_comment.db')
    c = db.cursor()

    query = 'Select comments from ins_comments where instructor_id = ?;'
    r = c.execute(query,[insid])
    resultsls = r.fetchall()

    sentences = []
    for i in range(len(resultsls)):
        sentence = resultsls[i][0]
        sentences.append(sentence)

    # clean up the sentences 
    resultsls = str(sentences)
    resultsls = resultsls.strip()
    resultsls = resultsls.replace("\\n","")
    r = re.compile("\[|\(|\)|\]|\\|\\\|;|:|'|,|\"|-|\'|\n|\\\\|\\\|\[|\']|")
    resultsls = re.sub(r, '', resultsls)
    resultsls = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', resultsls)
    db.close()
    return resultsls


def get_posneg_ls(ls, pos = True):
	'''
	given all comments list by instructor id, calculate sentiment score
	and divide the all sentences into prositive or negative list. 
	'''
    n_instances = 100
    subj_docs = [(sent, 'subj') for sent\
                 in subjectivity.sents(categories='subj')[:n_instances]]
    obj_docs = [(sent, 'obj') for sent\
                in subjectivity.sents(categories='obj')[:n_instances]]

    train_subj_docs = subj_docs[:80]
    test_subj_docs = subj_docs[80:100]
    train_obj_docs = obj_docs[:80]
    test_obj_docs = obj_docs[80:100]
    training_docs = train_subj_docs+train_obj_docs
    testing_docs = test_subj_docs+test_obj_docs
    sentim_analyzer = SentimentAnalyzer()
    all_words_neg = sentim_analyzer.all_words([mark_negation(doc)\
                                               for doc in training_docs])
    unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg,
                                                       min_freq=4)
    training_set = sentim_analyzer.apply_features(training_docs)
    test_set = sentim_analyzer.apply_features(testing_docs)
    trainer = NaiveBayesClassifier.train
    classifier = sentim_analyzer.train(trainer, training_set)
    sid = SentimentIntensityAnalyzer()
    
    neg_list = []
    pos_list = []
    for i in range(len(ls)):
        sentence = ls[i]
        ss = sid.polarity_scores(sentence)
        if ss['neg'] > ss['neu'] or ss['neg'] > ss['pos']:
            neg_list.append(sentence)
        else:
            pos_list.append(sentence)
    if pos:
        return pos_list
    else:
        return neg_list


def get_freq_ls(ls, n):
	'''
	given list of senteces, extract most comment n words.
	'''
    stops = nltk.corpus.stopwords.words('english')
    resultsls = str(ls)
    querywords = word_tokenize(resultsls)
    resultwords  = [word for word in querywords if word not in stops]
    result = ' '.join(resultwords)
    tagged_sent = pos_tag(result.split())
    # filter adjectives only
    adjectives = [word for word,pos in tagged_sent if pos == 'JJ' \
                or pos =='JJR' or pos =='JJS' or word == "\\" or word == '\['
                or word == '\]']
    freq_adj=nltk.FreqDist(adjectives)
    freq_adjls = freq_adj.most_common(n)

    freq_final = []
    for i in range(len(freq_adjls)):
        freq_final.append(freq_adjls[i][0])
    return freq_final


def extract(n):
	'''
	combine all functions above and extract top n positive and negative words
	by specific instructor id, and make in the form of dictionary of dictionary. 
	'''
    insid = find_insid()
    dict={}
    for iid in insid:
        print(iid)
        commentls = find_comments(iid)
        #get positive
        d = {}
        posls = get_posneg_ls(commentls, pos = True)
        pos_freqwords = get_freq_ls(posls, n)
        # get negative
        negls = get_posneg_ls(commentls, pos = False)
        neg_freqwords = get_freq_ls(negls, n)
        d['pos'] = pos_freqwords
        d['neg'] = neg_freqwords
        if iid not in dict:
            dict[iid] = d
    return dict