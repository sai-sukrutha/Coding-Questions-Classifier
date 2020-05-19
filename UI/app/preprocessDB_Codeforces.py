#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import ssl
import copy
import matplotlib.pyplot as plt
import re
import random

from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

from app import db
from app.models import User, Questions, QuestionTags
from config import Config


# tag list obtained from the dataset
tags_list = ['dsu', 'trees', 'chinese remainder theorem', 'sortings', 'games', 'implementation', 'bitmasks',
              '*special', 'hashing', 'geometry', 'two pointers', 'combinatorics', 'flows', 'strings',
              'probabilities', 'data structures', 'ternary search', 'greedy', 'math', 'matrices',
              'divide and conquer', 'dfs and similar', 'constructive algorithms', 'brute force', 'dp',
              '2-sat', 'graph matchings', 'binary search', 'number theory', 'graphs', 'fft', 'shortest paths',
              'schedules', 'meet-in-the-middle', 'string suffix structures', 'expression parsing']


def clean_statement(statement):
    statement = re.sub('$', ' ', statement)
    statement = re.sub('[^A-Za-z]+', ' ', statement)
    statement = re.sub('[,|.|?|\n]|\t', '', statement)
    statement = re.sub('n\'t', ' ', statement)
    statement = re.sub('submission|submissions|Submission|submission|th ', '', statement)
    statement = re.sub('one|two|given|need', '', statement)
    return statement


def process_problem_statement(q_statement):
    q_statement = clean_statement(q_statement)
    tokens = word_tokenize(q_statement)
    stoplist = set(stopwords.words('english'))
    word_list = [i for i in q_statement.lower().split() if i not in stoplist]
    ps = PorterStemmer()
    q_statement = ' '.join(word_list)
    return q_statement


def process_problem_solution(solution):
    tokens = word_tokenize(solution)
    stoplist = set(stopwords.words('english'))
    word_list = [i for i in solution.lower().split() if i not in stoplist]
    solution = ' '.join(word_list)
    return solution


def process_time_taken(time_col):
    return time_col.split()[0]


def process_tags(all_tags_list,tag_col):
    tags_present = list(re.split(',',tag_col))
    return tags_present


def data_preprocessing():
    print(Config.CODEFORCES_DATA_PATH)
    df = pd.read_csv(Config.CODEFORCES_DATA_PATH)
    df = df[df.solution != "no code found"]
    df = df.dropna()
    
    df["problem statement"] = [process_problem_statement(x) for x in df["problem statement"]]
    df["solution"] = [process_problem_solution(x) for x in df["solution"]]
    df["time_taken"] = [process_time_taken(x) for x in df["time_taken"]]
 
    return df


def process_data_to_db(data):
    rows = data.shape[0]
    ####
    prev_name = None
    for i in range(rows):
        #process row
        if( (i>=860 and i<910) or (i>=25480 and i<25830)):      #error for these indices
            continue
        qname = str(data['name'][i])
        if prev_name:
            if qname == prev_name:
                continue
        qcode = data.iloc[i].id
        qcode_contest = qcode[:-1]
        qcode_problem = qcode[-1]
        qlink = str(qcode_contest)+"/problem/"+str(qcode_problem)
        sol_link = str(qcode_contest)+"/submission/"+str(data['sol id'][i])
        platform = "codeforces"
        tags = data.iloc[i].tags
        tags_list = tags.split(',')
        #insert into db
        question = Questions(Qname=qname, Ques_link=qlink, Sol_link=sol_link, Platform=platform)
        db.session.add(question)
        db.session.flush()
        db.session.refresh(question)
        qid = question.Qid
        for tag in tags_list:
            tag_entry = QuestionTags(Tag=tag, Ques_id=qid)
            db.session.add(tag_entry)
        prev_name = qname
    db.session.commit()
    

def run():
    data = data_preprocessing()
    process_data_to_db(data)
