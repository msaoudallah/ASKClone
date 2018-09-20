from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


followers = db.Table('followers',
                db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
                db.Column('followed_id',db.Integer,db.ForeignKey('user.id'))
                )
    


class User(UserMixin, db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(60), index = True, unique=True)
    email = db.Column(db.String(120) , index = True, unique = True)
    password_hash = db.Column(db.String(128))
    asker = db.relationship('Question', backref = 'asker', lazy = 'dynamic', foreign_keys = 'Question.from_user_id')
    asked = db.relationship('Question', backref = 'asked', lazy = 'dynamic', foreign_keys = 'Question.to_user_id')

    followed = db.relationship('User',secondary=followers,
                            primaryjoin=followers.c.follower_id == id,
                            secondaryjoin = followers.c.followed_id == id,
                            backref = db.backref('followers',lazy='dynamic'),lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def is_following(self,user):
        return self.followed.filter(
            followers.c.followed_id == user.id
        ).count() > 0
    
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def followed_answered_questions(self):
        return Question.query.join(
            followers,(followers.c.followed_id == Question.to_user_id)).filter(
                followers.c.follower_id == self.id).filter(Question.answer != "").order(
                    Question.timestamp.desc())
            
    def followed_own_combined(self):
        followed= Question.query.join(
            followers,(followers.c.followed_id == Question.to_user_id)).filter(
                followers.c.follower_id == self.id).filter(Question.answer != "")
        own = Question.query.filter_by(to_user_id = self.id).filter(Question.answer != "")
        return followed.union(own)
        

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body  = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime , index = True , default = datetime.utcnow)
    answer = db.Column (db.String)
    from_user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    to_user_id = db.Column(db.Integer , db.ForeignKey('user.id'))


    def __repr__(self):
        return '<Q{} with body : {} asked from {} to {}>'.format(self.id, self.body, self.from_user_id, self.to_user_id)
    
    def answer_question(self,answer):
        self.answer = answer




