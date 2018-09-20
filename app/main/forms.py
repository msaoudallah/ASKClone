from flask_wtf import FlaskForm
from wtforms import  TextAreaField, SubmitField
from wtforms.validators import DataRequired
from app.models import User

class QuestionForm(FlaskForm):
    question = TextAreaField('write your question', validators=[DataRequired()])
    submit = SubmitField('ASK')

class AnswerForm(FlaskForm):
    answer = TextAreaField('write your answer' , validators=[DataRequired()])
    submit = SubmitField('Answer')

