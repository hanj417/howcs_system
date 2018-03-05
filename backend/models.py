import json
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from datetime import datetime, date
from ast import literal_eval
from backend import db, app

def date_from_str(date_str):
    if date_str is None:
        return
    date_list = list(map(int, date_str.split('-')))
    return date(date_list[0], date_list[1], date_list[2])

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))
    role = db.Column(db.String(128))
    name = db.Column(db.String(32))
    email = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    church = db.Column(db.String(32), nullable=True)
    school = db.Column(db.String(32), nullable=True)
    birthday = db.Column(db.Date(), nullable=True)
    student_info = relationship('StudentInfo', uselist=False, back_populates='user')
    agit_teacher_info = relationship('AgitTeacherInfo', uselist=False, back_populates='user')
    teaching_classes = relationship('Class', back_populates='teacher')
    attending_classes = relationship('Enrollment', back_populates='student')
    posts = relationship('Post', back_populates='author')
    payments = relationship('Payment', back_populates='user')
    attendances = relationship('Attendance', back_populates='student')
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=6000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def birthday_is(self, birthday_str):
        if birthday_str is None:
            return
        birthday_list = list(map(int, birthday_str.split('-')))
        self.birthday = date(birthday_list[0], birthday_list[1], birthday_list[2])

    def role_new(self, new_role):
        role = []
        if self.role:
            role = literal_eval(self.role)
        role.append(new_role)
        print(role)
        self.role = json.dumps(role)

    def role_del(self, del_role):
        role = []
        if self.role:
            role = literal_eval(self.role)
        role.remove(del_role)
        print(role)
        self.role = json.dumps(role)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def exist(username):
        return User.query.filter_by(username=username).first() is not None

    @staticmethod
    def default_role():
        return 'agit_student'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, ForeignKey('users.id'))
    title = db.Column(db.String(256))
    major_category = db.Column(db.String(64))
    minor_category = db.Column(db.String(64))
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    approval = db.Column(db.Boolean, default=False)
    time_slot = db.Column(db.String(64), nullable=True)
    audience = db.Column(db.String(64), nullable=True)
    background = db.Column(db.UnicodeText(), nullable=True)
    content = db.Column(db.UnicodeText(), nullable=True)
    teacher = relationship('User', back_populates='teaching_classes')
    students = relationship('Enrollment', back_populates='class_')
    attendances = relationship('Attendance', back_populates='class_')
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    def required_columns(self):
        return ['teacher_id', 'title', 'major_category', 'minor_category', 'year', 'semester']
    def as_dict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dic['teacher'] = self.teacher.as_dict()
        return dic
    @staticmethod
    def major_categories():
        return [{'text':'홈페이지', 'value':'homepage'}, {'text':'아지트', 'value':'agit'}, {'text':'하나', 'value':'hana'}]

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    class_id = db.Column(db.Integer, ForeignKey('classes.id'), primary_key=True)
    student_id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True)
    approval = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    class_ = relationship('Class', back_populates='students')
    student = relationship('User', back_populates='attending_classes')
    def required_columns(self):
        return ['class_id', 'student_id']
    def as_dict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dic['class'] = self.class_.as_dict()
        dic['student'] = self.student.as_dict()
        return dic

class StudentInfo(db.Model):
    __tablename__ = 'student_infos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    student_id = db.Column(db.String(32))
    gender = db.Column(db.String(32))
    ssn = db.Column(db.String(32))
    father_name = db.Column(db.String(32))
    father_ssn = db.Column(db.String(32))
    mother_name = db.Column(db.String(32))
    mother_ssn = db.Column(db.String(32))
    address = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    user = relationship('User', back_populates='student_info')
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class AgitTeacherInfo(db.Model):
    __tablename__ = 'agit_teacher_infos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    approval = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    user = relationship('User', back_populates='agit_teacher_info')
    def as_dict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dic['user'] = self.user.as_dict()
        return dic

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    major_category = db.Column(db.String(64))
    minor_category = db.Column(db.String(64))
    properties = db.Column(db.String(256))
    title = db.Column(db.String(256))
    body = db.Column(db.UnicodeText())
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    author = relationship('User', back_populates='posts')
    def required_columns(self):
        return ['major_category', 'minor_category', 'title', 'body']
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    @staticmethod
    def major_categories():
        return [{'text':'홈페이지', 'value':'homepage'}, {'text':'아지트', 'value':'agit'}, {'text':'하나', 'value':'hana'}]
    @staticmethod
    def properties_list():
        return [{'text':'공지', 'value':'notice'}]
    

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    cost = db.Column(db.Integer)
    category = db.Column(db.String(64))
    year = db.Column(db.Integer, nullable=True)
    semester = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    user = relationship('User', back_populates='payments')
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Attendance(db.Model):
    __tablename__ = 'attendances'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, ForeignKey('classes.id'))
    student_id = db.Column(db.Integer, ForeignKey('users.id'))
    date = db.Column(db.Date())
    category = db.Column(db.String(64))
    description = db.Column(db.UnicodeText(), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    class_ = relationship('Class', back_populates='attendances')
    student = relationship('User', back_populates='attendances')
    def required_columns(self):
        return ['class_id', 'student_id', 'date', 'category']
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    @staticmethod
    def categories():
        return ['출석', '결석', '지각']

    

'''
class Parent(db.Model):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), ForeignKey('users.username'))
    parent_id = db.Column(db.String(32))
    
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    user = relationship('User', backref=backref('students', order_by=id))
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), ForeignKey('users.username'))
    career = db.Column(db.UnicodeText())
    user = relationship('User', backref=backref('teachers', order_by=id))

class StudentRecord(db.Model):
    __tablename__ = 'student_records'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), ForeignKey('users.username'))
    year = db.Column(db.Integer)
    content = db.Column(db.UnicodeText())
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    student = relationship('Student', backref=backref('student_records', order_by=id))

'''

