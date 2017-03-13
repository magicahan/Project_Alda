#Project ALDA
#@ Alice Mee Seon Chung

import nltk
import sqlite3
import re
from nltk.tag import *
from nltk.corpus import stopwords
from nltk.sentiment import *
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment.util import *


def find_comments(insid):
    db = sqlite3.connect('ins_comment.db')
    c = db.cursor()

    query = 'Select comments from ins_comments where instructor_id = ?;'
    r = c.execute(query,[insid])
    resultsls = r.fetchall()

    sentences = []
    for i in range(len(resultsls)):
        sentence = resultsls[i][0]
        sentences.append(sentence)
    resultsls = str(sentences)
    resultsls = resultsls.strip()
    r = re.compile("\[|\(|\)|\]|\\|\\|;|:|'|,|\"|-|'|")
    resultsls = re.sub(r, '', resultsls)
    resultsls = resultsls.replace("\\n","")
    resultsls = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', resultsls)
    db.close()
    
    return resultsls


def get_posneg_ls(ls, pos = True):
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
    stops = nltk.corpus.stopwords.words('english')
    resultsls = str(ls)
    querywords = resultsls.lower().split()
    resultwords  = [word for word in querywords if word not in stops]
    result = ' '.join(resultwords)
    tagged_sent = pos_tag(result.split())
    adjectives = [word for word,pos in tagged_sent if pos == 'JJ' \
             or pos =='JJR' or pos =='JJS' or pos =='RB' or pos =='RBR' \
             or pos =='RBS' or pos =='JJ']
    freq_adj=nltk.FreqDist(adjectives)
    freq_adjls = freq_adj.most_common(n)

    freq_final = []
    for i in range(len(freq_adjls)):
        freq_final.append(freq_adjls[i][0])
    return freq_final