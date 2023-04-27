
from datetime import datetime, timedelta, timezone
from hashlib import md5
from app import app, db, login
import jwt

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    comment = db.relationship('Show_info_comment', backref='comment_author'
                                                           '', lazy='dynamic')

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, followers.c.followed_id == Post.user_id
        ).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({"reset_password": self.id,
                           "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)},
                          app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")[
                "reset_password"]
        except:           
            return None
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'<Post {self.body}>'


class Show(db.Model):
    __tablename__ ='show'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140),unique=True)#show name
    img = db.Column(db.String(140)) #show img url
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)#time for creating
    info_id = db.relationship('Show_info',backref='show',lazy='dynamic')# the show info of this
    comment_id = db.relationship('Show_info_comment',backref='which_show',lazy='dynamic')# the show info of this
    def __repr__(self) -> str:
        return f'<Show {self.name} {self.timestamp} {self.info_id} {self.comment_id}>'


class Show_info(db.Model):
    __tablename__= 'show_info'
    id = db.Column(db.Integer, primary_key=True)

    show_id = db.Column(db.Integer, db.ForeignKey('show.id'),unique=True)#info belong to show
    no = db.Column(db.Integer)                      # number of show
    text = db.Column(db.Text())                     #the information

    def __repr__(self) -> str:
        return f'<Show_info {self.show_id} {self.no} {self.text} >'

class Show_info_comment(db.Model):
    __tablename__= 'Show_info_comment'
    id = db.Column(db.Integer, primary_key=True)

    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))#评论所属节目
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#评论所属人员
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)#评论时间戳
    text = db.Column(db.Text())

    def __repr__(self) -> str:
        return f'{self.id}< Coment: show_id: {self.show_id} user_id: {self.user_id} comment: {self.text} {self.timestamp} >'
