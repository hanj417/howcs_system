import json
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from datetime import datetime, date, timedelta
from ast import literal_eval
from backend import db, app
from bs4 import BeautifulSoup

def date_from_str(date_str):
    if date_str is None:
        return
    date_list = list(map(int, date_str.split('-')))
    return date(date_list[0], date_list[1], date_list[2])

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

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
    parent_info = relationship('ParentInfo', uselist=False, back_populates='user')
    agit_teacher_info = relationship('AgitTeacherInfo', uselist=False, back_populates='user')
    howcs_teacher_info = relationship('HowcsTeacherInfo', uselist=False, back_populates='user')
    #children = relationship('FamilyRelation', back_populates='parent')
    #parents = relationship('FamilyRelation', back_populates='child')

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
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if self.student_info:
            dic['student_info'] = self.student_info.as_dict()
        return dic

class Privilege(db.Model):
    __tablename__ = 'privileges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    label = db.Column(db.String(32))
    user = db.Column(db.Boolean, default=False)
    user_new = db.Column(db.Boolean, default=False)
    user_update = db.Column(db.Boolean, default=False)
    user_del = db.Column(db.Boolean, default=False)
    student = db.Column(db.Boolean, default=False)
    student_new = db.Column(db.Boolean, default=False)
    student_update = db.Column(db.Boolean, default=False)
    student_del = db.Column(db.Boolean, default=False)
    howcs_teacher = db.Column(db.Boolean, default=False)
    howcs_teacher_new = db.Column(db.Boolean, default=False)
    howcs_teacher_update = db.Column(db.Boolean, default=False)
    howcs_teacher_del = db.Column(db.Boolean, default=False)
    howcs_class = db.Column(db.Boolean, default=False)
    howcs_class_new = db.Column(db.Boolean, default=False)
    howcs_class_update = db.Column(db.Boolean, default=False)
    howcs_class_del = db.Column(db.Boolean, default=False)
    howcs_enrollment = db.Column(db.Boolean, default=False)
    howcs_enrollment_new = db.Column(db.Boolean, default=False)
    howcs_enrollment_update = db.Column(db.Boolean, default=False)
    howcs_enrollment_del = db.Column(db.Boolean, default=False)
    howcs_attendance = db.Column(db.Boolean, default=False)
    howcs_attendance_new = db.Column(db.Boolean, default=False)
    howcs_attendance_update = db.Column(db.Boolean, default=False)
    howcs_attendance_del = db.Column(db.Boolean, default=False)
    howcs_post = db.Column(db.Boolean, default=False)
    howcs_post_new = db.Column(db.Boolean, default=False)
    howcs_post_update = db.Column(db.Boolean, default=False)
    howcs_post_del = db.Column(db.Boolean, default=False)
    homepage_post = db.Column(db.Boolean, default=False)
    homepage_post_new = db.Column(db.Boolean, default=False)
    homepage_post_update = db.Column(db.Boolean, default=False)
    homepage_post_del = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    def as_dict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return dic

    @staticmethod
    def exist(name_or_label):
        if Privilege.query.filter_by(name=name_or_label).first() is not None:
            return True
        if Privilege.query.filter_by(label=name_or_label).first() is not None:
            return True
        return False


class FamilyRelation(db.Model):
    __tablename__ = 'family_relations'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.String(32), ForeignKey('users.id'))
    child_id = db.Column(db.String(32), ForeignKey('users.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    #parent = relationship('User', foreign_keys=[parent_id], back_populates='children')
    #child = relationship('User', foreign_keys=[child_id], back_populates='parents')
    parent = relationship('User', foreign_keys=[parent_id], backref='children')
    child = relationship('User', foreign_keys=[child_id], backref='parents')
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class StudentInfo(db.Model):
    __tablename__ = 'student_infos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    student_id = db.Column(db.String(32))
    gender = db.Column(db.String(32), nullable=True)
    rrn = db.Column(db.String(32), nullable=True)
    father_name = db.Column(db.String(32), nullable=True)
    father_rrn = db.Column(db.String(32), nullable=True)
    mother_name = db.Column(db.String(32), nullable=True)
    mother_rrn = db.Column(db.String(32), nullable=True)
    address = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    user = relationship('User', back_populates='student_info')
    student_record = relationship('StudentRecord', back_populates="student_info", uselist=False)
    def as_dict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if self.student_record:
            dic['student_record'] = self.student_record.as_dict()
        return dic

class ParentInfo(db.Model):
    __tablename__ = 'parent_infos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    user = relationship('User', back_populates='parent_info')
    def as_dict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if self.student_records:
            dic['student_records'] = self.student_records.as_dict()
        return dic

class AgitTeacherInfo(db.Model):
    __tablename__ = 'agit_teacher_infos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    career = db.Column(db.UnicodeText()) 
    approval = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    user = relationship('User', back_populates='agit_teacher_info')
    def as_dict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dic['user'] = self.user.as_dict()
        return dic

class HowcsTeacherInfo(db.Model):
    __tablename__ = 'howcs_teacher_infos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    user = relationship('User', back_populates='howcs_teacher_info')
    def as_dict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dic['user'] = self.user.as_dict()
        return dic

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    class_id = db.Column(db.Integer, ForeignKey('classes.id'), nullable=True)
    major_category = db.Column(db.String(64))
    minor_category = db.Column(db.String(64))
    properties = db.Column(db.String(256))
    title = db.Column(db.String(256))
    body = db.Column(db.UnicodeText())
    files = db.Column(db.UnicodeText(), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    author = relationship('User', back_populates='posts')
    class_ = relationship('Class', back_populates='posts')
    def required_columns(self):
        return ['major_category', 'minor_category', 'title', 'body']
    def properties_new(self, new_properties):
        properties = []
        if self.properties:
            properties = literal_eval(self.properties)
        properties.append(new_properties)
        print(properties)
        self.properties = json.dumps(properties)

    def properties_del(self, del_properties):
        properties = []
        if self.properties:
            properties = literal_eval(self.properties)
        properties.remove(del_properties)
        print(properties)
        self.properties = json.dumps(properties)

    def as_dict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if self.author:
            dic['author'] = self.author.as_dict()
        if self.class_:
            dic['class'] = self.class_.as_dict()
        soup = BeautifulSoup(dic['body']) 
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        dic['ellipsis'] = text[:100]
        return dic

    def created_at_is(self, created_at_str):
        if created_at_str is None or created_at_str == '':
            return
        print (created_at_str)
        created_at_str = created_at_str.split('T')[0]
        created_at_list = list(map(int, created_at_str.split('-')))
        self.created_at = datetime(created_at_list[0], created_at_list[1], created_at_list[2])

    @staticmethod
    def major_categories():
        return [{'label':'홈페이지', 'value':'homepage'}, {'label':'아지트', 'value':'agit'}, {'label':'하우학교', 'value':'howcs'}]
    @staticmethod
    def minor_categories():
        return {'homepage': [
                    {'label':'공지', 'value':'notice'},
                    {'label':'하우하다', 'value':'story'},
                    {'label':'하우포토', 'value':'photo'}],
                'agit': [
                    {'label':'청소년', 'value':'teenager'},
                    {'label':'문학', 'value':'literature'},
                    {'label':'성인', 'value':'adult'}],
                'howcs': [
                    {'label':'교육자료', 'value':'edu_resource'},
                    {'label':'교무자료', 'value':'academic_resource'},
                    {'label':'수업', 'value':'subject'},
                    {'label':'학급', 'value':'class'}]}
    @staticmethod
    def properties_list():
        return [{'text':'공지', 'value':'notice'}]
    
class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, ForeignKey('users.id'))
    title = db.Column(db.String(256))
    major_category = db.Column(db.String(64))
    minor_category = db.Column(db.String(64))
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer, nullable=True)
    approval = db.Column(db.Boolean, default=False)
    time_slot = db.Column(db.String(64), nullable=True)
    audience = db.Column(db.String(64), nullable=True)
    background = db.Column(db.UnicodeText(), nullable=True)
    content = db.Column(db.UnicodeText(), nullable=True)
    google_calendar = db.Column(db.String(256), nullable=True)
    teacher = relationship('User', back_populates='teaching_classes')
    students = relationship('Enrollment', back_populates='class_')
    attendances = relationship('Attendance', back_populates='class_')
    posts = relationship('Post', back_populates='class_')
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    def required_columns(self):
        return ['teacher_id', 'title', 'major_category', 'minor_category']
    def as_dict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if self.teacher:
            dic['teacher'] = self.teacher.as_dict()
        return dic
    @staticmethod
    def major_categories():
        return [{'label':'아지트', 'value':'agit'}, {'label':'하우학교', 'value':'howcs'}]
    @staticmethod
    def minor_categories():
        return {'homepage': [
                    {'label':'공지', 'value':'notice'},
                    {'label':'하우하다', 'value':'story'},
                    {'label':'하우포토', 'value':'photo'}],
                'agit': [
                    {'label':'청소년', 'value':'teenager'},
                    {'label':'문학', 'value':'literature'},
                    {'label':'성인', 'value':'adult'}],
                'howcs': [
                    {'label':'부모학교', 'value':'parent_school'},
                    {'label':'수업', 'value':'subject'},
                    {'label':'학급', 'value':'class'}]}

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
        return ['class_id']
    def as_dict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dic['class'] = self.class_.as_dict()
        dic['student'] = self.student.as_dict()
        return dic

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

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    cost = db.Column(db.Integer)
    major_category = db.Column(db.String(64))
    year = db.Column(db.Integer, nullable=True)
    semester = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Date())
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    user = relationship('User', back_populates='payments')
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class StudentRecord(db.Model):
    __tablename__ = 'student_records'
    id = db.Column(db.Integer, primary_key=True)
    student_info_id = db.Column(db.Integer, ForeignKey('student_infos.id'))
    student_info = relationship('StudentInfo', back_populates='student_record')
    student_annual_records = relationship('StudentAnnualRecord', back_populates='student_record')
    student_award_records = relationship('StudentAwardRecord', back_populates='student_record')
    student_school_registration_records = relationship('StudentSchoolRegistrationRecord', back_populates='student_record')
    student_health_records = relationship('StudentHealthRecord', back_populates='student_record')
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    def as_dict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if self.student_annual_records:
            dic['student_annual_records'] = []
            for student_annual_record in self.student_annual_records:
                dic['student_annual_records'].append(student_annual_record.as_dict())
        if self.student_award_records:
            dic['student_award_records'] = []
            for student_award_record in self.student_award_records:
                dic['student_award_records'].append(student_award_record.as_dict())
        if self.student_school_registration_records:
            dic['student_school_registration_records'] = []
            if student_school_registration_record in self.student_school_registration_records:
                dic['student_school_registration_records'].append(student_school_registration_record.as_dict())
        if self.student_health_records:
            dic['student_health_records'] = []
            for student_health_record in self.student_health_records:
                dic['student_health_records'].append(student_health_record.as_dict())
        return dic

class StudentSchoolRegistrationRecord(db.Model):
    __tablename__ = 'student_school_registration_records'
    id = db.Column(db.Integer, primary_key=True)
    student_record_id = db.Column(db.Integer, ForeignKey('student_records.id'))
    school = db.Column(db.String(64))
    content = db.Column(db.UnicodeText())
    date = db.Column(db.Date(), nullable=True)
    student_record = relationship('StudentRecord', back_populates='student_school_registration_records')
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class StudentAwardRecord(db.Model):
    __tablename__ = 'student_award_records'
    id = db.Column(db.Integer, primary_key=True)
    student_record_id = db.Column(db.Integer, ForeignKey('student_records.id'))
    content = db.Column(db.UnicodeText())
    date = db.Column(db.Date(), nullable=True)
    student_record = relationship('StudentRecord', back_populates='student_award_records')
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class StudentAnnualRecord(db.Model):
    __tablename__ = 'student_annual_records'
    id = db.Column(db.Integer, primary_key=True)
    student_record_id = db.Column(db.Integer, ForeignKey('student_records.id'))
    year = db.Column(db.Integer)
    content = db.Column(db.UnicodeText())

    student_record = relationship('StudentRecord', back_populates='student_annual_records')
    student_attendance_records = relationship('StudentAttendanceRecord', back_populates='student_annual_record')
    student_reading_records = relationship('StudentReadingRecord', back_populates='student_annual_record')
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    def as_dict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if self.student_attendance_records:
            dic['student_attendance_records'] = self.student_attendance_records.as_dict()
        if self.student_reading_records:
            dic['student_reading_records'] = self.student_reading_records.as_dict()
        return dic

class StudentAttendanceRecord(db.Model):
    __tablename__ = 'student_attendance_records'
    id = db.Column(db.Integer, primary_key=True)
    student_annual_record_id = db.Column(db.Integer, ForeignKey('student_annual_records.id'))

    school_days = db.Column(db.Integer)
    absence = db.Column(db.Integer)
    early_leave = db.Column(db.Integer)
    lateness = db.Column(db.Integer)
    absence_illness = db.Column(db.Integer)
    absence_wo_notice = db.Column(db.Integer)
    lateness_illness = db.Column(db.Integer)
    lateness_wo_notice = db.Column(db.Integer)
    early_leave_illness = db.Column(db.Integer)
    early_leave_wo_notice = db.Column(db.Integer)

    note = db.Column(db.UnicodeText())

    student_annual_record = relationship('StudentAnnualRecord', back_populates='student_attendance_records')
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class StudentReadingRecord(db.Model):
    __tablename__ = 'student_reading_records'
    id = db.Column(db.Integer, primary_key=True)
    student_annual_record_id = db.Column(db.Integer, ForeignKey('student_annual_records.id'))
    title = db.Column(db.String(256))
    content = db.Column(db.UnicodeText())
    date = db.Column(db.Date(), nullable=True)
    student_annual_record = relationship('StudentAnnualRecord', back_populates='student_reading_records')
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class StudentHealthRecord(db.Model):
    __tablename__ = 'student_health_records'
    id = db.Column(db.Integer, primary_key=True)
    student_record_id = db.Column(db.Integer, ForeignKey('student_records.id'))
    date = db.Column(db.Date(), nullable=True)
    internal_medicine = db.Column(db.UnicodeText())
    dental_clinic = db.Column(db.UnicodeText())
    fluorine_coating = db.Column(db.UnicodeText())
    height = db.Column(db.String(256))
    weight = db.Column(db.String(256))
    sight = db.Column(db.String(256))
    internal_medicine_content = db.Column(db.UnicodeText())
    cavity = db.Column(db.UnicodeText())
    dental_clinic_content = db.Column(db.UnicodeText())
    content = db.Column(db.UnicodeText())
    student_record = relationship('StudentRecord', back_populates='student_health_records')
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    def date_is(self, date_str):
        if date_str is None:
            return
        date_str = date_str.split('T')[0]
        date_list = list(map(int, date_str.split('-')))
        self.date = date(date_list[0], date_list[1], date_list[2])

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

