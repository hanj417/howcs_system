#!/usr/bin/env python
import os
import math
import json
from flask import Flask, render_template, jsonify, abort, request, g, url_for
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from random import *
import datetime

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
assets = Environment(app)
assets.append_path('./dist/assets')

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

def _get_date():
    return datetime.datetime.now()

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
    student_id = db.Column(db.String(32), nullable=True)
    sex = db.Column(db.String(32), nullable=True)
    ssn = db.Column(db.String(32), nullable=True)
    father_name = db.Column(db.String(32), nullable=True)
    father_ssn = db.Column(db.String(32), nullable=True)
    mother_name = db.Column(db.String(32), nullable=True)
    mother_ssn = db.Column(db.String(32), nullable=True)
    address = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.Date(), default=_get_date)
    updated_at = db.Column(db.Date(), onupdate=_get_date)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

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

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Type(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/api/login', methods=['POST'])
@auth.verify_password
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    user = User.verify_auth_token(username)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):
            abort(400)    # missing arguments
    g.user = user
    token = g.user.generate_auth_token(600)
    user_info = {
        'username': username,
        'password': password,
        'avatar': '@image',
        'nickname': '@name',
        'created_at': '@datetime',
        'updated_at': '@datetime'
    }
    return jsonify({'token': token.decode('ascii'), 'duration': 600, 'user': user_info})
    

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/menu')
def get_menu():
    menu = [
        { 'header': 'Admin' },
        { 'href': '/', 'title': 'Home', 'icon': 'home' },
        #{ 'href': '/crud/types', 'title': 'Types', 'icon': 'view_list' },
        #{ 'href': '/crud/posts', 'title': 'Posts', 'icon': 'view_list' },
        #{ 'href': '/crud/posts/create', 'title': 'Create Post', 'icon': 'note_add' },
        #{ 'href': '/crud/comments', 'title': 'Comments', 'icon': 'view_list' },
        { 'href': '/crud/users', 'title': 'Users', 'icon': 'people' },
        { 'href': '/login', 'icon': 'lock', 'title': 'Logout' }]
    return jsonify(menu)

@app.route('/api/topMenu')
def get_top_menu():
    menu = [
        { 'header': 'Admin' },
        { 'href': '/', 'title': 'Home', 'icon': 'home' },
        { 'href': '/crud/users', 'title': 'Users', 'icon': 'people' },
        { 'href': '/register', 'icon': 'lock', 'title': 'Register' },
        { 'href': '/login', 'icon': 'lock', 'title': 'Logout' }]
    return jsonify(menu)

@app.route('/api/users/form')
def get_users_form():
    user_id = int(request.args.get('id', 0))
    user = User.query.get(user_id)
    users_form = {
        'fields': {
            'username': {
                'label': 'Username',
                'required': True
            },
            'email': {
                'label': 'Email',
                'required': True
            },
            'phone': {
                'label': 'Phone',
                'required': False
            }
        }
    }
    if user:
        users_form['model'] = user.as_dict
    else:
        users_form['model'] = {'username':'', 'email':'', 'phone':''}
    return jsonify(users_form)

@app.route('/api/settings/form')
def get_settings_form():
    settings_form = {
        'model': {
            'name': 'Adminify',
            'logo': 'http://placeimg.com/128/128/any',
            'type': 1,
            'status': 1,
            'tags': [],
            'description': 'An Awesome Site',
            'intro': ''
        },
        'fields': {
            'name': {'label': 'Name'},
            'logo': {'label': 'Logo', 'type': 'image'},
            'date': {'label': 'Created At', 'type': 'datetime'},
            'type': {'label': 'Type',
                'type': 'select',
                'options': [
                    {'text': 'Blog', 'value': 1},
                    {'text': 'Company', 'value': 2},
                    {'text': 'Game', 'value': 3}
                ]},
            'status': {'label': 'Status',
                'type': 'radios',
                'width': 'md3',
                'options': [
                    {'text': 'Enabled', 'value': 1},
                    {'text': 'Disabled', 'value': 2}
                ]},
            'tags': {'label': 'Tags',
                'type': 'checkboxes',
                'width': 'md3',
                'options': [
                    {'text': 'Vue', 'value': 1},
                    {'text': 'React', 'value': 2},
                    {'text': 'Angular', 'value': 3}
                    ]},
            'description': {'label': 'Description(Textarea)', 'type': 'textarea'},
            'intro': {'label': 'Intro', 'type': 'html'}
        }
    }
    return jsonify(settings_form)

@app.route('/api/types/form')
def get_types_form():
    types_form = {
        #'model': data.types[params.id - 1],
        'fields': {
            'name': {
                'label': 'Name',
                'required': True
            }
        }
    }
    return jsonify(types_form)

@app.route('/api/posts/form')
def get_posts_form():
    posts_form = {}
    '''
        'model': params.id ? data.posts[params.id - 1] : {
            type_id: null,
            title: null,
            body: null
        },
        'fields': {
            'type_id': {
                'type': 'select',
                'label': 'Type',
                'required': true,
                'options': data.choices('types')
            },
            'title': {
                'label': 'title',
                'required': true
            },
            'body': {
                'label': 'Body',
                'type': 'html'
            }
        }
    }
    '''
    return jsonify(posts_form)

@app.route('/api/users/grid')
def get_users_grid():
    users_grid = {
        'options': {
            'sort': '-id',
            'create': True,
            'update': True,
            'delete': True
        },
        'filters': {
            'model': {
                'username': '',
            },
            'fields': {
                'username': {
                    'label': 'Username'
                },
            },
            'rules': {}
        },
        'columns': [
            {
                'text': 'Id',
                'value': 'id'
            },
            {
                'text': 'Username',
                'left': True,
                'value': 'username'
            },
            {
                'text': 'Email',
                'left': True,
                'value': 'email'
            },
            {
                'text': 'Phone',
                'left': True,
                'value': 'phone'
            }
        ]
    }
    return jsonify(users_grid)

@app.route('/api/users', methods=['POST'])
def user_new():
    username = request.json.get('username')
    password = request.json.get('password')
    name = request.json.get('name')
    email = request.json.get('email')
    phone = request.json.get('phone')
    church = request.json.get('church')
    school = request.json.get('school')
    birthday = request.json.get('birthday')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    user.name = name
    user.email = email
    user.phone = phone
    user.church = church
    user.school = school
    user.birthday = birthday 
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}))


@app.route('/api/users')
def get_user_all():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    users = User.query.all()
    offset = (page - 1) * per_page
    users_json = []
    for user in users:
        users_json.append(user.as_dict())
    result = {
        'currentPage': page,
        'lastPage': math.ceil(len(users) / per_page),
        'perPage': per_page,
        'total': len(users),
        'data': users_json[offset:(offset + per_page)]
    }
    return jsonify(result)

@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

def _new_admin():
    username = 'admin'
    password = '123456'
    if User.query.filter_by(username=username).first() is not None:
        return
    user = User(username=username)
    user.hash_password(password)
    user.name = '관리자'
    user.role = json.dumps(['admin'])
    user.email = 'hanj417@gmail.com'
    user.phone = '010-8896-5121'
    user.church = '하늘빛우리교회'
    user.school = '하우학교'
    user.birthday = _get_date()
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    _new_admin()
    app.run(host='0.0.0.0', port=3000, debug=False)
