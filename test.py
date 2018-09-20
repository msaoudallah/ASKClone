from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Question


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    

    def test_follow(self):
        u1 = User(username = 'ali', email = 'ali@example.com')
        u2 = User(username = 'h', email = 'h@example.com')

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u1.followed.all(),[])
        self.assertEqual(u1.followers.all(),[])

        u1.follow(u2)

        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(),1)
        self.assertEqual(u1.followed.first().username,'h')
        self.assertEqual(u2.followers.count(),1)
        self.assertEqual(u2.followers.first().username,'ali')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

        

    def test_followed_questions(self):
        u1 = User(username = 'ali', email = 'ali@example.com')
        u2 = User(username = 'h', email = 'h@example.com')
        u3 = User(username = 'emad', email = 'emad@example.com')
        u4 = User(username = 'essam', email = 'essam@example.com')
        db.session.add_all([u1,u2,u3,u4])

        db.session.commit()

        # create questions 
        now = datetime.utcnow()

        q1 = Question(body = 'how r u u3 ? ', answer ="", timestamp= now+timedelta(seconds=1),
        asker = u2, asked = u3 )

        q2 = Question(body = 'sa3a kam ? ', answer ="5 w nos", timestamp= now+timedelta(seconds=2),
        asker = u2, asked = u3 )

        q3 = Question(body = 'omk 3amla eih ? ', answer ="a7sn mn omk", timestamp= now+timedelta(seconds=3),
        asker = u1, asked = u3 )

        q4 = Question(body = 'asasddasas ? ', answer ="dddd", timestamp= now+timedelta(seconds=4),
        asker = u2, asked = u1 )

        q5 = Question(body = 'fel tagamo3 w by7sl kda ? ', answer ="fuck femenism", timestamp= now+timedelta(seconds=5),
        asker = u4, asked = u3 )

        q6 = Question(body = 'zamalek ? ', answer ="7oby", timestamp= now+timedelta(seconds=6),
        asker = u3, asked = u2 )

        q7 = Question(body = 'zamalek ? ', answer ="", timestamp= now+timedelta(seconds=7),
        asker = u4, asked = u1 )

        db.session.add_all([q1,q2,q3,q4,q5,q6,q7])
        db.session.commit()


        u1.follow(u3)
        u4.follow(u1)
        db.session.commit()

        f1 = u1.followed_own_combined().all()
        f2 = u2.followed_own_combined().all()
        f3 = u3.followed_own_combined().all()
        f4 = u4.followed_own_combined().all()
        

        self.assertEqual(f1,[q2,q3,q4,q5])
        self.assertEqual(f2,[q6])
        self.assertEqual(f3,[q2,q3,q5])
        self.assertEqual(f4,[q4])



if __name__ == '__main__':
    unittest.main(verbosity=2)
        
        
