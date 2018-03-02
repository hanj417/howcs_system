import math
from flask import Flask, render_template, jsonify, abort, request, g, url_for
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from backend import app
from backend.models import *
from flask import make_response

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)

@basic_auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@token_auth.verify_token
def verify_token(username_or_token):
    user = User.verify_auth_token(username_or_token)
    if not user:
        return False
    g.user = user
    return True

@app.route('/api/login', methods=['POST'])
@multi_auth.login_required
def login():
    token = g.user.generate_auth_token(600)
    user_info = g.user.as_dict()
    return jsonify({'user': user_info, 'token': token.decode('ascii')})

@app.route('/api/token')
@multi_auth.login_required
def auth_token_new():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

##################################################
# user 
##################################################
@app.route('/api/users', methods=['GET'])
#@multi_auth.login_required
def user_all():
    #FIXME
    #return jsonify
    #users = User.query.all()
    #users_json = []
    #for user in users:
    #    users_json.append(user.as_dict())
    #return users_json
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    if 'name' in request.args:
        users = User.query.filter_by(name=request.args['name']).all()
    else:
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

@app.route('/api/users', methods=['POST'])
def user_new():
    if not request.json or not 'username' in request.json or not 'password' in request.json:
        abort(400)

    username = request.json.get('username')
    if User.exist(username):
        abort(400)    # existing user

    user = User(username=username)
    user.password = user.hash_password(request.json.get('password'))
    user.role_new(User.default_role())
    user.name = request.json.get('name')
    user.email = request.json.get('email')
    user.phone = request.json.get('phone')
    user.church = request.json.get('church')
    user.school = request.json.get('school')
    user.birthday_is(request.json.get('birthday'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'user': user.as_dict()}), 201

@app.route('/api/users/<int:id>', methods=['GET'])
#@multi_auth.login_required
def user_get(id):
    user = User.query.get(id)
    if not user:
        abort(404)

    user_dict = user.as_dict()
    '''
    if 'howcs_student' in user.role:
        student = Student.query.filter_by(username=user.username).first()
        student_profile = student.as_dict()
        profile.update(student_profile)
    '''
    return jsonify(user_dict)

@app.route('/api/users/<int:id>', methods=['PUT'])
#@multi_auth.login_required
def user_update(id):
    if not request.json:
        abort(400)
    user = User.query.get(id)
    if not user:
        abort(404)

    user.username = request.json.get('username')
    password = request.json.get('password')
    if password:
        user.hash_password(password)
    user.name = request.json.get('name', user.name)
    user.email = request.json.get('email', user.email)
    user.phone = request.json.get('phone', user.phone)
    user.church = request.json.get('church', user.church)
    user.school = request.json.get('school', user.school)
    user.birthday_is(request.json.get('birthday'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'user': user.as_dict()})

@app.route('/api/users/<int:id>', methods=['DELETE'])
#@multi_auth.login_required
def user_del(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'result': True})


##################################################
# class
##################################################
@app.route('/api/classes', methods=['GET'])
#@multi_auth.login_required
def class_all():
    #FIXME
    #return jsonify
    #classes = Class.query.all()
    #classes_json = []
    #for class_ in classes:
    #    classes_json.append(class_.as_dict())
    #return classes_json
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    classes = Class.query.all()
    offset = (page - 1) * per_page
    classes_json = []
    for class_ in classes:
        classes_json.append(class_.as_dict())
    result = {
        'currentPage': page,
        'lastPage': math.ceil(len(classes) / per_page),
        'perPage': per_page,
        'total': len(classes),
        'data': classes_json[offset:(offset + per_page)]
    }
    return jsonify(result)

@app.route('/api/classes', methods=['POST'])
def class_new():
    if not request.json:
        abort(400)

    class_ = Class()
    print(class_.required_columns())
    for column in class_.required_columns():
        if column not in request.json:
            abort(400)

    teacher_username = request.json.get('teacher')
    teacher = User.query.filter_by(username=teacher_username).first()
    if not teacher:
        abort(404)
    
    class_.teacher_id = teacher.id
    class_.teacher = teacher
    class_.title = request.json.get('title')
    class_.category = request.json.get('category')
    class_.year = int(request.json.get('year'))
    class_.semester = int(request.json.get('semester'))
    class_.time_slot = request.json.get('time_slot')
    class_.audience = request.json.get('audience')
    class_.background = request.json.get('background')
    class_.content = request.json.get('content')
    db.session.add(class_)
    db.session.commit()
    return jsonify({'class': class_.as_dict()}), 201

@app.route('/api/classes/<int:id>', methods=['GET'])
#@multi_auth.login_required
def class_get(id):
    class_ = Class.query.get(id)
    if not class_:
        abort(404)
    class_dict = class_.as_dict()
    return jsonify(class_dict)

@app.route('/api/classes/<int:id>', methods=['PUT'])
#@multi_auth.login_required
def class_update(id):
    if not request.json:
        abort(400)
    class_ = Class.query.get(id)
    if not class_:
        abort(404)

    teacher_username = request.json.get('teacher', class_.teacher.username)
    teacher = User.query.filter_by(username=teacher_username).first()
    if not teacher:
        abort(404)
    
    class_.teacher_id = teacher.id
    class_.teacher = teacher
    class_.title = request.json.get('title', class_.title)
    class_.category = request.json.get('category', class_.category)
    class_.year = int(request.json.get('year', class_.year))
    class_.semester = int(request.json.get('semester', class_.semester))
    class_.time_slot = request.json.get('time_slot', class_.time_slot)
    class_.audience = request.json.get('audience', class_.audience)
    class_.background = request.json.get('time_slot', class_.background)
    class_.content = request.json.get('content', class_.content)
    db.session.add(class_)
    db.session.commit()
    return jsonify({'class_': class_.as_dict()})

@app.route('/api/classes/<int:id>', methods=['DELETE'])
#@multi_auth.login_required
def class_del(id):
    class_ = Class.query.get(id)
    if not class_:
        abort(404)
    db.session.delete(class_)
    db.session.commit()
    return jsonify({'result': True})


##################################################
# enrollment 
##################################################
@app.route('/api/enrollments', methods=['GET'])
#@multi_auth.login_required
def enrollmentall():
    #FIXME
    #return jsonify
    #enrollments = Enrollment.query.all()
    #enrollments_json = []
    #for enrollment in enrollments:
    #    enrollments_json.append(enrollment.as_dict())
    #return enrollments_json
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    offset = (page - 1) * per_page
    if 'class' in request.args:
        enrollments = Enrollment.query.filter_by(class_id=request.args['class']).all()
    else:
        enrollments = Enrollment.query.all()
    enrollments_json = []
    for enrollment in enrollments:
        enrollments_json.append(enrollment.as_dict())
    result = {
        'currentPage': page,
        'lastPage': math.ceil(len(enrollments) / per_page),
        'perPage': per_page,
        'total': len(enrollments),
        'data': enrollments_json[offset:(offset + per_page)]
    }
    return jsonify(result)

@app.route('/api/enrollments', methods=['POST'])
def enrollment_new():
    if not request.json:
        abort(400)

    enrollment = Enrollment()
    print(enrollment.required_columns())
    for column in enrollment.required_columns():
        if column not in request.json:
            abort(400)

    enrollment.class_id = request.json.get('class_id')
    enrollment.student_id = request.json.get('student_id')
    enrollment.approval = False
    enrollment.student = User.query.filter_by(id = enrollment.student_id).first()
    class_ = Class.query.filter_by(id = enrollment.class_id).first()
    class_.students.append(enrollment)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'enrollment': enrollment.as_dict()}), 201

@app.route('/api/enrollments/<int:id>', methods=['GET'])
#@multi_auth.login_required
def enrollmentget(id):
    enrollment = Enrollment.query.get(id)
    if not enrollment:
        abort(404)
    enrollmentdict = enrollment.as_dict()
    return jsonify(enrollmentdict)

@app.route('/api/enrollments/<int:id>', methods=['PUT'])
#@multi_auth.login_required
def enrollmentupdate(id):
    if not request.json:
        abort(400)
    enrollment = Enrollment.query.get(id)
    if not enrollment:
        abort(404)

    teacher_username = request.json.get('teacher', enrollment.teacher.username)
    teacher = User.query.filter_by(username=teacher_username).first()
    if not teacher:
        abort(404)
    
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'enrollment': enrollment.as_dict()})

@app.route('/api/enrollments/<int:class_id>/<int:student_id>', methods=['DELETE'])
#@multi_auth.login_required
def enrollment_del(class_id, student_id):
    enrollment = Enrollment.query.filter_by(class_id = class_id, student_id = student_id).first()
    if not enrollment:
        abort(404)
    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({'result': True})




##################################################
# post 
##################################################
@app.route('/api/posts/major_categories')
def get_posts_major_categories():
    categories = Post.major_categories()
    return jsonify(categories)

@app.route('/api/posts/properties')
def get_posts_properties():
    properties = Post.properties_list()
    return jsonify(properties)

@app.route('/api/posts', methods=['GET'])
#@multi_auth.login_required
def post_all():
    #FIXME
    #return jsonify
    #posts = Post.query.all()
    #posts_json = []
    #for post in posts:
    #    posts_json.append(post.as_dict())
    #return posts_json
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    offset = (page - 1) * per_page
    if 'major_category' in request.args:
        if 'minor_category' in request.args:
            posts = Post.query.filter_by(major_category=request.args['major_category'], minor_category=request.args['minor_category']).all()
        else:
            posts = Post.query.filter_by(major_category=request.args['major_category']).all()
    elif 'author_id' in request.args:
        posts = Post.query.filter_by(author_id=request.args['author_id']).all()
    else:
        posts = Post.query.all()
    posts_json = []
    for post in posts:
        posts_json.append(post.as_dict())
    result = {
        'currentPage': page,
        'lastPage': math.ceil(len(posts) / per_page),
        'perPage': per_page,
        'total': len(posts),
        'data': posts_json[offset:(offset + per_page)]
    }
    return jsonify(result)

@app.route('/api/posts', methods=['POST'])
def post_new():
    if not request.json:
        abort(400)

    post = Post()
    print(post.required_columns())
    for column in post.required_columns():
        if column not in request.json:
            abort(400)

    post.author_id = request.json.get('author_id', 1)
    post.major_category = request.json.get('major_category')
    post.minor_category = request.json.get('minor_category')
    post.properties = json.dumps(request.json.get('properties'))
    post.title = request.json.get('title')
    post.body = request.json.get('body')

    author = User.query.filter_by(id = post.author_id).first()
    post.author = author
    db.session.add(post)
    db.session.commit()
    return jsonify({'post': post.as_dict()}), 201

@app.route('/api/posts/<int:id>', methods=['GET'])
#@multi_auth.login_required
def post_get(id):
    post = Post.query.get(id)
    if not post:
        abort(404)
    postdict = post.as_dict()
    return jsonify(postdict)

@app.route('/api/posts/<int:id>', methods=['PUT'])
#@multi_auth.login_required
def post_update(id):
    if not request.json:
        abort(400)
    post = Post.query.get(id)
    if not post:
        abort(404)

    post.author_id = request.json.get('author_id', post.author_id)
    post.major_category = request.json.get('major_category', post.major_category)
    post.minor_category = request.json.get('minor_category', post.minor_category)
    post.properties = json.dumps(request.json.get('properties', post.properties))
    post.title = request.json.get('title', post.title)
    post.body = request.json.get('body', post.body)

    author = User.query.filter_by(id = post.author_id).first()
    
    db.session.add(post)
    db.session.commit()
    return jsonify({'post': post.as_dict()})

@app.route('/api/posts/<int:id>', methods=['DELETE'])
#@multi_auth.login_required
def post_del(id):
    post = Post.query.filter_by(id = id).first()
    if not post:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'result': True})


'''

@app.route('/api/students', methods=['POST'])
#@multi_auth.login_required
def student_new():
    username = request.json.get('username')
    password = request.json.get('password')
    name = request.json.get('name')
    email = request.json.get('email')
    phone = request.json.get('phone')
    church = request.json.get('church')
    school = request.json.get('school')
    birthday = request.json.get('birthday')
    student_id = request.json.get('student_id')
    gender = request.json.get('gender')
    ssn = request.json.get('ssn')
    father_name = request.json.get('father_name')
    father_ssn = request.json.get('father_ssn')
    mother_name = request.json.get('mother_name')
    mother_ssn = request.json.get('mother_ssn')
    address = request.json.get('address')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    if Student.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    user.role = json.dumps(['agit_student', 'howcs_student'])
    user.name = name
    user.email = email
    user.phone = phone
    user.church = church
    user.school = school
    birthday_list = list(map(int, birthday.split('-')))
    user.birthday = datetime.date(birthday_list[0], birthday_list[1], birthday_list[2])
    student = Student(username=username)
    student.birthday = datetime.date(birthday_list[0], birthday_list[1], birthday_list[2])
    student.student_id = student_id
    student.gender = gender
    student.ssn = ssn
    student.father_name = father_name
    student.father_ssn = father_ssn
    student.mother_name = mother_name
    student.mother_ssn = mother_ssn
    student.address = address
    db.session.add(user)
    db.session.add(student)
    db.session.commit()
    return (jsonify({'username': user.username}))

@app.route('/api/students/update', methods=['POST'])
#@multi_auth.login_required
def student_update():
    username = request.json.get('username')
    password = request.json.get('password')
    name = request.json.get('name')
    email = request.json.get('email')
    phone = request.json.get('phone')
    church = request.json.get('church')
    school = request.json.get('school')
    birthday = request.json.get('birthday')
    student_id = request.json.get('student_id')
    gender = request.json.get('gender')
    ssn = request.json.get('ssn')
    father_name = request.json.get('father_name')
    father_ssn = request.json.get('father_ssn')
    mother_name = request.json.get('mother_name')
    mother_ssn = request.json.get('mother_ssn')
    address = request.json.get('address')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is None:
        abort(400)    # existing user
    if Student.query.filter_by(username=username).first() is None:
        abort(400)    # existing user

    user = g.user
    if User.query.filter_by(username=username).first() != user:
        abort(400)    # existing user
    student = Student.query.filter_by(username=username).first()

    if password:
        user.hash_password(password)
    user.name = name
    user.email = email
    user.phone = phone
    user.church = church
    user.school = school
    birthday_list = list(map(int, birthday.split('-')))
    user.birthday = datetime.date(birthday_list[0], birthday_list[1], birthday_list[2])

    student.student_id = student_id
    student.gender = gender
    student.ssn = ssn
    student.father_name = father_name
    student.father_ssn = father_ssn
    student.mother_name = mother_name
    student.mother_ssn = mother_ssn
    student.address = address
    db.session.add(user)
    db.session.add(student)
    db.session.commit()
    return (jsonify({'username': user.username}))


@app.route('/api/students/update/<int:id>', methods=['POST'])
#@multi_auth.login_required
def student_edit(id):
    username = request.json.get('username')
    password = request.json.get('password')
    name = request.json.get('name')
    email = request.json.get('email')
    phone = request.json.get('phone')
    church = request.json.get('church')
    school = request.json.get('school')
    birthday = request.json.get('birthday')
    student_id = request.json.get('student_id')
    gender = request.json.get('gender')
    ssn = request.json.get('ssn')
    father_name = request.json.get('father_name')
    father_ssn = request.json.get('father_ssn')
    mother_name = request.json.get('mother_name')
    mother_ssn = request.json.get('mother_ssn')
    address = request.json.get('address')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is None:
        abort(400)    # existing user

    user = User.query.get(id)
    if not user:
        abort(400)


    if password:
        user.hash_password(password)
    user.name = name
    user.email = email
    user.phone = phone
    user.church = church
    user.school = school
    birthday_list = list(map(int, birthday.split('-')))
    user.birthday = datetime.date(birthday_list[0], birthday_list[1], birthday_list[2])

    if Student.query.filter_by(username=username).first() is None:
        student = Student(username=username)
        if 'howcs_student' not in user.role:
            user.role = [x.strip().strip('"') for x in user.role.strip("[").strip("]").split(',')]
            print (user.role)
            user.role.append('howcs_student')
            user.role = json.dumps(user.role)
    else:
        student = Student.query.filter_by(username=username).first()
    student.birthday = datetime.date(birthday_list[0], birthday_list[1], birthday_list[2])
    student.student_id = student_id
    student.gender = gender
    student.ssn = ssn
    student.father_name = father_name
    student.father_ssn = father_ssn
    student.mother_name = mother_name
    student.mother_ssn = mother_ssn
    student.address = address
    db.session.add(user)
    db.session.add(student)
    db.session.commit()
    return (jsonify({'username': user.username}))


@app.route('/api/students')
#@multi_auth.login_required
def get_students_all():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    offset = (page - 1) * per_page
    users_json = []
    for user, student in db.session.query(User, Student).filter(User.username == Student.username).all():
        user_dict = student.as_dict()
        user_dict.update(user.as_dict())
        users_json.append(user_dict)
        print(users_json)
    result = {
        'currentPage': page,
        'lastPage': math.ceil(len(users_json) / per_page),
        'perPage': per_page,
        'total': len(users_json),
        'data': users_json[offset:(offset + per_page)]
    }
    return jsonify(result)

@app.route('/api/students/delete', methods=['POST'])
#@multi_auth.login_required
def delete_student():
    id = request.json.get('id')
    user = User.query.get(id)
    if not user:
        abort(400)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'id': user.username})

'''

@app.route('/api/menu')
def get_menu():
    menu = [
        { 'href': 'main', 'params': {}, 'text': 'Home', 'icon': 'home' },
        { 'href': 'user_form', 'params': {'action':'update'}, 'text': '회원정보', 'icon': 'home' },
        { 'href': 'user', 'params': {}, 'text': '아지트회원', 'icon': 'home' },
        { 'href': 'class', 'params': {}, 'text': '학급', 'icon': 'home' },
        { 'href': 'post', 'params': {}, 'text': '글', 'icon': 'home' },
        { 'href': 'student', 'params': {}, 'text': 'Student', 'icon': 'home' },
        #{ 'href': '/crud/types', 'text': 'Types', 'icon': 'view_list' },
        #{ 'href': '/crud/posts', 'text': 'Posts', 'icon': 'view_list' },
        #{ 'href': '/crud/posts/create', 'text': 'Create Post', 'icon': 'note_add' },
        #{ 'href': '/crud/comments', 'text': 'Comments', 'icon': 'view_list' },
        #{ 'href': '/crud/users', 'text': 'Users', 'icon': 'people' },
    ]
    return jsonify(menu)

@app.route('/api/toolbar')
def get_toolbar():
    toolbar = [
        { 'header': 'Admin' },
        { 'href': '/', 'text': 'Home', 'icon': 'home' },
        #{ 'href': '/crud/users', 'text': 'Users', 'icon': 'people',
        #  'children': [
        #        { 'href': '/', 'text': 'Home', 'icon': 'home' },
        #  ],
        #},
        { 'href': '/user_form/new', 'icon': 'lock', 'text': 'Register' },
        { 'href': '/login', 'icon': 'lock', 'text': 'Login' }
    ]
    return jsonify(toolbar)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@basic_auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
