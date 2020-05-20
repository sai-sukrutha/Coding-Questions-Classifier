import os


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATA_PATH = basedir + '/data'
    CODECHEF_DATA_PATH = DATA_PATH + '/codechef_questions.csv'
    CODEFORCES_DATA_PATH = DATA_PATH + '/codeforces_question_v5.csv'

    codechef_question_link = "https://www.codechef.com/problems/"
    codechef_solution_link = "http://discuss.codechef.com/problems/"

    codeforces_question_link = "https://codeforces.com/contest/"
    codeforces_solution_link = "https://codeforces.com/contest/"

    MODEL_PATH = basedir + '/modeldata/'
    MODEL_FILE = MODEL_PATH + 'bert-model.pkl'
    LE_FILE = MODEL_PATH + 'le.pkl'
    LB_FILE = MODEL_PATH + 'lb.pkl'
