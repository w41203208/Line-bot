from sqlalchemy.orm import backref
from . import db
from sqlalchemy.sql import func


class Protein(db.Model):
    __tablename__ = 'protein'

    proteinId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proteinName = db.Column(db.Text)
    proteinDesc = db.Column(db.Text)
    foods = db.relationship('Food', backref='food')

class Food(db.Model):
    __tablename__ = 'food'

    foodId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    foodName = db.Column(db.Text(150))
    foodTag = db.Column(db.Text)
    foodKcal = db.Column(db.Float)
    foodProtein = db.Column(db.Float)
    foodNaa = db.Column(db.Float)
    foodKa = db.Column(db.Float)
    foodP = db.Column(db.Float)
    foodCarbohydrate = db.Column(db.Float)
    foodProteinId = db.Column(db.Integer, db.ForeignKey('protein.proteinId'))

class Member(db.Model):
    __tablename__ = 'member'

    memberId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.Text(100))
    Sex = db.Column(db.Text(10))
    Age = db.Column(db.Integer)
    phoneNumber = db.Column(db.String(150))
    password = db.Column(db.String(150))
    dateTime = db.Column(db.DateTime)
    diseaseTypes = db.relationship('DiseaseType', backref='diseasetype')
    bloodPressures = db.relationship('BloodPressure', backref='bloodpressure')
    bloodSugars = db.relationship('BloodSugar', backref='bloodsugar')
    posts = db.relationship('Post', backref='post')
    messages = db.relationship('Message', backref='message')

class DiseaseType(db.Model):
    __tablename__ = 'diseasetype'

    memberId = db.Column(db.Integer, db.ForeignKey('member.memberId'))#待討論
    diseaseId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    typeName = db.Column(db.Text)

class BloodPressure(db.Model):
    __tablename__ = 'bloodpressure'

    memberId = db.Column(db.Integer, db.ForeignKey('member.memberId'))
    bpId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sp = db.Column(db.Float)
    dp = db.Column(db.Float)
    mbp = db.Column(db.Float)
    dateTime = db.Column(db.DateTime)

class BloodSugar(db.Model):
    __tablename__ = 'bloodsugar'

    memberId = db.Column(db.Integer, db.ForeignKey('member.memberId'))
    bsId  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sugarValue = db.Column(db.Float)
    dateTime = db.Column(db.DateTime)

class Post(db.Model):
    __tablename__ = 'post'

    memberId = db.Column(db.Integer, db.ForeignKey('member.memberId'))
    postId  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    imgSrc = db.Column(db.Text)
    postTitle = db.Column(db.Text)
    postLike = db.Column(db.Boolean)#待討論
    dateTime = db.Column(db.DateTime)

class Message(db.Model):
    __tablename__ = 'message'

    memberId = db.Column(db.Integer, db.ForeignKey('member.memberId'))
    postId  = db.Column(db.Integer, db.ForeignKey('post.postId'))
    messageId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    messageContent = db.Column(db.Text)
    messageLike = db.Column(db.Boolean)#待討論
    dateTime = db.Column(db.DateTime)







