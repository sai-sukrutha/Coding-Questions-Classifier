from app import app, db, login
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, QuestionForm, TagForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Questions, QuestionTags
from werkzeug.urls import url_parse
from datetime import datetime

from config import Config
from app import model_predictions

class Questiondata:
    def __init__(self, qname, ques_link, sol_link):
        self.qname = qname
        self.ques_link = ques_link
        if sol_link:
            self.sol_link = sol_link
        else:
            self.sol_link = None


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    else:
        print(form.errors)
    return render_template('register.html', title='Register', form=form)


@app.route('/find_questiontag', methods=['GET', 'POST'])
@login_required
def find_questiontag():
    form = QuestionForm()
    if form.validate_on_submit():
        question = form.question.data
        # print(question)
        tags = model_predictions.run(question)
        tags = tags[0].strip('[]')
        tags_list = tags.split(',')

        final_tags = []
        for tag in tags_list:
            final_tags.append(tag.strip().strip('\''))

        tags_str = ',  '.join(final_tags)

        return render_template('print_questiontag.html',tags=tags_str,question=question)
    return render_template('find_questiontag.html', form=form)


@app.route('/get_tagquestions', methods=['GET', 'POST'])
@login_required
def get_tagquestions():
    form = TagForm()
    if form.validate_on_submit():
        tag = form.tag.data
        tag = tag.lower()
        print(tag)
        if( tag == 'dynamic programming'):
            tag = "dp"
        if( tag == 'dfs'):
            tag = "dfs and similar"
        if( tag == "mst" or tag == "minimum shortest path" or tag == "minimum shortest paths"):
            tag = "shortest paths"
        if(tag == "tree"):
            tag = "trees"
        if(tag == "graph"):
            tag = "graphs"
        if(tag == "maths"):
            tag = "math"
        if(tag == "matrix"):
            tag = "matrices"
        all_data = QuestionTags.query.filter(QuestionTags.Tag==tag).all()
        #dividing codechef and codeforces
        cc_data = []
        cf_data = []
        for d in all_data:
            qid = d.Ques_id
            question = Questions.query.filter(Questions.Qid==qid).first()
            qname = question.Qname
            ques_link = question.Ques_link
            sol_link = question.Sol_link
            if question.Platform == 'codechef':
                ques_link = Config.codechef_question_link + ques_link
                if sol_link:
                    sol_link = Config.codechef_solution_link + sol_link
                else:
                    sol_link = None
                q_data = Questiondata(qname, ques_link, sol_link)
                cc_data.append(q_data)
            elif question.Platform == 'codeforces':
                ques_link = Config.codeforces_question_link + ques_link
                sol_link = Config.codeforces_solution_link + sol_link
                q_data = Questiondata(qname, ques_link, sol_link)
                cf_data.append(q_data)
        return render_template('print_tagquestions.html',tag=tag,cc_data=cc_data,cf_data=cf_data)
    return render_template('get_tagquestions.html', form=form)


