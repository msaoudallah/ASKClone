from app import db
from app.main import bp
from app.main.forms import QuestionForm, AnswerForm
from flask import render_template, redirect, url_for, request, flash
from app.models import User, Question
from flask_login import current_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    user = User.query.filter_by(username = current_user.username).first()
    questions = User.followed_own_combined(user)
    return render_template('index.html', questions = questions)


@bp.route('/ask/<username>', methods=['GET', 'POST'])
@login_required
def ask(username):
    user = User.query.filter_by(username = username).first()
    form = QuestionForm()

    if form.validate_on_submit():
        question = Question(body = form.question.data, 
        timestamp = datetime.utcnow(), 
        answer = '', 
        from_user_id= current_user.id,
        to_user_id = user.id)

        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.ask',username=username))

        #return redirect(url_for('user',username=username))
    return render_template('ask.html', form=form)





@bp.route('/user/<username>', methods=['GET'])
@login_required
def user(username):
    user = User.query.filter_by(username= username).first_or_404()
    questions = Question.query.filter_by(to_user_id = user.id).all()

    
    answered_questions = [q for q in questions if q.answer !="" ]


    if username != current_user.username :
        questions_list = answered_questions
    else :
        questions_list = questions

    return render_template('user.html',user=user,questions =questions_list)



@bp.route('/answer', methods=['GET', 'POST'])
@login_required
def answer():
    question_id = request.args.get('id')
    username = request.args.get('username')
    question = Question.query.filter_by(id = question_id).first()
    if question.answer != "" :
            return redirect(url_for('main.user',username=username))
    form = AnswerForm()
    if form.validate_on_submit():
        question.answer = form.answer.data
        db.session.commit()
        return redirect(url_for('main.user',username=username))
    return render_template('answer.html', form=form, question = question)


@bp.route('/explore', methods = ['GET'])
@login_required
def explore():
    q = Question.query.filter(Question.answer !='').all()
    return render_template('index.html',questions = q)



@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username = username).first()

    if user is None :
        flash('user {} is not found'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('you can\'t follow yourself')
        return redirect(url_for('main.user', username= username))
    
    current_user.follow(user)
    db.session.commit()
    flash('you are now following{}'.format(username))
    return redirect(url_for('main.user', username = username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username = username).first()

    if user is None :
        flash('user {} is not found'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('you can\'t unfollow yourself')
        return redirect(url_for('main.user', username= username))
    
    current_user.unfollow(user)
    db.session.commit()
    flash('you are now not following{}'.format(username))
    return redirect(url_for('main.user', username = username))