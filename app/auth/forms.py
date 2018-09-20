from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError 
from app.models import User



class SignUpForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired()])
    password2 = PasswordField('re-enter password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('signup')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')


