from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='manh', email='manhdk@wepass.vn')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/9d467334383a91cc3acea542e29e5cf7?d=identicon&s=128'))
    
    def test_follow(self):
        u1 = User(username='manh', email='manhdk@wepass.vn')
        u2 = User(username='john', email='john@wepass.vn')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'john')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'manh')

    def test_follow_posts(self):
        u1 = User(username='john', email='john@wepass.vn')
        u2 = User(username='susan', email='susan@wepass.vn')
        u3 = User(username='mary', email='mary@wepass.vn')
        u4 = User(username='david', email='david@wepass.vn')
        db.session.add_all([u1, u2, u3, u4])
        
        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="john", user_id=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="susan", user_id=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", user_id=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", user_id=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # manh follows susan
        u1.follow(u4)  # manh follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == "__main__":
    unittest.main(verbosity=2)
