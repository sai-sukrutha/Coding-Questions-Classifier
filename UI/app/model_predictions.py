import os
import collections
import pandas as pd
import numpy as np
import joblib

from config import Config

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

from app import model,lb,le


def clean_question(question):
    question = question.lower()
    q_words = word_tokenize(question)
    stop = stopwords.words('english')
    clean_words = [w for w in q_words if not w in stop] 
    clean_ques = ' '.join(clean_words)
    # print(clean_ques) 
    return clean_ques


def get_prediction(model, lb, le, question):
    question = clean_question(question)
    predictions, raw_outputs = model.predict([question])
    y=lb.inverse_transform( raw_outputs, threshold=0.1)
    y=le.inverse_transform(y)
    return y


def run(question):
    # model, lb, le = get_modeldata()
    y = get_prediction(model, lb, le, question)
    y_list = y.tolist()
    return y_list


'''
Chef Ciel is playing a game with one of her colleagues.In this game, there are k piles of numbers. There are ni numbers in ith pile. In each move, player has to select a pile and finally a number from that pile. After that, all the numbers which are greater than or equal to chosen number will be removed from that pile. Players take turn alternatively. Player who is unable to move loses the game. 
Chef Ciel always make first move. But before making her move, she must choose either EVEN or ODD. If she chooses even then each time she selects a number it must be even and her opponent must select odd number in his/her turn. And vice versa for the other case. 
Please help Chef Ciel to make her choice. If neither choice can make her win game, print DONT PLAY otherwise EVEN or ODD depending on which choice she should make to win game. If you think then you will understand BOTH can not be answer.
Assume that both players play intelligently, if they can force win they will. 
 Input :  First line of test case contains t, number of test cases. Then t test cases follow. First line of each test case contains k, number of piles.  Then description of k piles follow. ith pile description contains number ni, then ni numbers follow in the same line.
Output :  Print EVEN, ODD or DONT PLAY accordingly.
Constraints :  t <= 1000, k <=100, ni <= 45. Numbers in pile will be non-negative and less than 2^31.
Sample Input :
2
2 
2 3 4
2 4 5
1
3 1 2 3
Sample Output :
DONT PLAY ODD
Explanation: 
In the first test case, if you have chosen ODD to play with, it means you will select only ODD numbers and your opponent may choose only EVEN numbers. So you have two options. Either select 3 from first pile or 5 from second pile. If 3 is selected, 3 and 4 are removed from first pile and in next move your opponents only move will be 4 from second pile removing every numbers thus you lose. If you had selected 5, then your opponents optimal move would be selecting 4 from first pile. Next you will select 3 and your opponent 4 leaving nothing for you. So if you choose ODD you will lose. Similarly if you choose EVEN you will lose as well. So the answer is DONT Play.
In the second case, if you choose ODD just select 1 and you will win. If you choose EVEN you have only one move that is 2, and in response your opponent will choose 1 and leave you nothing. Thus answer is ODD.
'''
