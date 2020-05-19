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
    if type(statement)!= str:
        return statement
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
#     solution = clean_statement(solution)
    tokens = word_tokenize(solution)
    stoplist = set(stopwords.words('english'))
    word_list = [i for i in solution.lower().split() if i not in stoplist]
    solution = ' '.join(word_list)
    return solution


def process_tags(tag_col):
#     tags_present = list(re.split(',',tag_col))
    stoplist = set(stopwords.words('english'))
    word_list = [i for i in solution.lower().split() if i not in stoplist]
    
    tags_set = set(tags_present)
    tags_diff = tags_set.difference(set(all_tags_list))
    
    new_set = tags_set.difference(tags_diff)
    return list(new_set)


def process_problem_Languages(lang_col):
    lang_col = clean_statement(lang_col)
    return lang_col


def validate_tags(tags):
    global tags_list
    tags = eval(tags)
    i = 0
    while i<len(tags):
        if tags[i] not in tags_list:
            tags.remove(tags[i])
            continue
        i += 1
    return tags


def data_preprocessing():
    print(Config.CODECHEF_DATA_PATH)
    df = pd.read_csv(Config.CODECHEF_DATA_PATH,encoding="ISO-8859-1")
    df["Languages"] = [process_problem_Languages(x) for x in df["Languages"]]
    for index, row in df.iterrows():
        tags = validate_tags(row['Tags'])
        if tags == []:
            df.drop(index, inplace=True)
        else:
            df.at[index, 'Tags'] = str(tags)   
    return df


def process_data_to_db(data):
    rows = data.shape[0]
    ####
    for i in range(rows):
        #process row
        qcode = data.iloc[i].QCode
        qname = data.iloc[i].Title
        qlink = qcode
        sol_link = None
        if type(data.iloc[i].Editorial) == type("  "):
            sol_link = qcode
        platform = "codechef"
        tags = data.iloc[i].Tags
        tags = tags.strip('[]')
        tags_list = tags.split(',')
        tags_list = [ t.strip().strip('\'') for t in tags_list]
        #insert into db
        if sol_link:
            question = Questions(Qname=qname, Ques_link=qlink, Sol_link=sol_link, Platform=platform)
        else:
            question = Questions(Qname=qname, Ques_link=qlink, Sol_link=None, Platform=platform)
        db.session.add(question)
        db.session.flush()
        db.session.refresh(question)
        qid = question.Qid
        for tag in tags_list:
            tag_entry = QuestionTags(Tag=tag, Ques_id=qid)
            db.session.add(tag_entry)
    db.session.commit()

    

def run():
    data = data_preprocessing()
    process_data_to_db(data)



    
    


