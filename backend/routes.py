import math
from flask import Flask, render_template, jsonify, abort, request, g, url_for
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from flask_mail import Message
from backend import app
from backend import mail
from backend.models import *
from flask import make_response

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)

def mail_to_admin():
    msg = Message("Hello",
                  recipients=["hanj417@gmail.com"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    mail.send(msg)

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
@multi_auth.login_required
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
@multi_auth.login_required
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
@multi_auth.login_required
def user_del(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'result': True})

##################################################
# agit_teachers
##################################################
@app.route('/api/agit_teacher_infos', methods=['GET'])
@multi_auth.login_required
def agit_teacher_infos_all():
    user = g.user
    if not user:
        abort(400)
    if 'admin' not in user.role:
        abort(400)

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    offset = (page - 1) * per_page
    agit_teacher_infos = AgitTeacherInfo.query
    agit_teacher_infos = agit_teacher_infos.all()
    agit_teacher_infos_json = []
    for agit_teacher_info in agit_teacher_infos:
        agit_teacher_infos_json.append(agit_teacher_info.as_dict())
    result = {
        'currentPage': page,
        'lastPage': math.ceil(len(agit_teacher_infos) / per_page),
        'perPage': per_page,
        'total': len(agit_teacher_infos),
        'data': agit_teacher_infos_json[offset:(offset + per_page)]
    }
    return jsonify(result)

@app.route('/api/agit_teacher_infos', methods=['POST'])
@multi_auth.login_required
def agit_teacher_infos_new():
    user = g.user
    if not user:
        abort(400)

    agit_teacher_info = AgitTeacherInfo()
    agit_teacher_info.user_id = user.id
    agit_teacher_info.approval = False
    agit_teacher_info.user = user
    user.agit_teacher_info = agit_teacher_info

    db.session.add(agit_teacher_info)
    db.session.add(user)
    db.session.commit()
    return jsonify({'agit_teacher_info': agit_teacher_info.as_dict()}), 201

@app.route('/api/agit_teacher_infos/<int:id>', methods=['PUT'])
@multi_auth.login_required
def agit_teacher_info_update(id):
    user = g.user
    if not user:
        abort(400)
    if 'admin' not in user.role:
        abort(400)
    if not request.json:
        abort(400)
    agit_teacher_info = AgitTeacherInfo.query.get(id)
    if not agit_teacher_info:
        abort(404)

    agit_teacher_info.approval = request.json.get('approval', agit_teacher_info.approval)

    if agit_teacher_info.approval == True:
        agit_teacher_info.user.role_new('agit_teacher')
    if agit_teacher_info.approval == False:
        agit_teacher_info.user.role_del('agit_teacher')
         

    db.session.add(agit_teacher_info)
    db.session.commit()
    return jsonify({'agit_teacher_info': agit_teacher_info.as_dict()})

@app.route('/api/agit_teacher_infos/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def agit_teacher_info_del(id):
    user = g.user
    if not user:
        abort(400)
    if 'admin' not in user.role:
        abort(400)
    agit_teacher_info = AgitTeacherInfo.query.get(id)
    if not agit_teacher_info:
        abort(404)

    db.session.delete(agit_teacher_info)
    db.session.commit()
    return jsonify({'result': True})


##################################################
# howcs_teachers
##################################################
@app.route('/api/howcs_teacher_infos', methods=['GET'])
@multi_auth.login_required
def howcs_teacher_infos_all():
    user = g.user
    if not user:
        abort(400)
    if 'admin' not in user.role:
        abort(400)

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    offset = (page - 1) * per_page
    howcs_teacher_infos = HowcsTeacherInfo.query
    howcs_teacher_infos = howcs_teacher_infos.all()
    howcs_teacher_infos_json = []
    for howcs_teacher_info in howcs_teacher_infos:
        howcs_teacher_infos_json.append(howcs_teacher_info.as_dict())
    result = {
        'currentPage': page,
        'lastPage': math.ceil(len(howcs_teacher_infos) / per_page),
        'perPage': per_page,
        'total': len(howcs_teacher_infos),
        'data': howcs_teacher_infos_json[offset:(offset + per_page)]
    }
    return jsonify(result)

@app.route('/api/howcs_teacher_infos', methods=['POST'])
@multi_auth.login_required
def howcs_teacher_infos_new():
    user = g.user
    if not user:
        abort(400)
    if 'admin' not in user.role:
        abort(400)

    howcs_teacher_info = HowcsTeacherInfo()
    howcs_teacher_info.user_id = request.json.get('user_id')
    user = User.query.filter_by(id = howcs_teacher_info.user_id).first()
    howcs_teacher_info.user = user
    user.role_new('howcs_teacher')

    db.session.add(howcs_teacher_info)
    db.session.commit()
    return jsonify({'user': user.as_dict()}), 201

@app.route('/api/howcs_teacher_infos/<int:id>', methods=['PUT'])
@multi_auth.login_required
def howcs_teacher_info_update(id):
    user = g.user
    if not user:
        abort(400)
    if 'admin' not in user.role:
        abort(400)
    if not request.json:
        abort(400)
    howcs_teacher_info = HowcsTeacherInfo.query.get(id)
    if not howcs_teacher_info:
        abort(404)


    db.session.add(howcs_teacher_info)
    db.session.commit()
    return jsonify({'howcs_teacher_info': howcs_teacher_info.as_dict()})

@app.route('/api/howcs_teacher_infos/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def howcs_teacher_info_del(id):
    user = g.user
    if not user:
        abort(400)
    if 'admin' not in user.role:
        abort(400)
    howcs_teacher_info = HowcsTeacherInfo.query.get(id)
    if not howcs_teacher_info:
        abort(404)

    howcs_teacher_info.user.role_del('howcs_teacher')

    db.session.delete(howcs_teacher_info)
    db.session.commit()
    return jsonify({'result': True})

##################################################
# student
##################################################
@app.route('/api/student_infos')
#@multi_auth.login_required
def get_student_infos_all():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    offset = (page - 1) * per_page

    student_infos = StudentInfo.query.all()
    users = []
    for student_info in student_infos:
        users.append(student_info.user)
    users_json = []
    for user in users:
        users_json.append(user.as_dict())
    result = {
        'currentPage': page,
        'lastPage': math.ceil(len(users_json) / per_page),
        'perPage': per_page,
        'total': len(users_json),
        'data': users_json[offset:(offset + per_page)]
    }
    return jsonify(result)

@app.route('/api/student_infos', methods=['POST'])
@multi_auth.login_required
def student_new():
    if 'admin' not in g.user.role:
        abort(400)

    if not request.json or not 'username' in request.json or not 'password' in request.json:
        abort(400)

    username = request.json.get('username')
    if User.exist(username):
        abort(400)    # existing user
    if Student.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user

    birthday = request.json.get('birthday')

    user = User(username=username)
    user.password = user.hash_password(request.json.get('password'))
    user.role_new(User.default_role())
    user.role_new('agit_student')
    user.name = request.json.get('name')
    user.email = request.json.get('email')
    user.phone = request.json.get('phone')
    user.church = request.json.get('church')
    user.school = request.json.get('school')
    user.birthday_is(request.json.get('birthday'))

    student = StudentInfo()
    student.user_id = user.id
    student.student_id = request.json.get('student_id')
    student.gender = request.json.get('gender')
    student.ssn = request.json.get('ssn')
    student.father_name = request.json.get('father_name')
    student.father_ssn = request.json.get('father_ssn')
    student.mother_name = request.json.get('mother_name')
    student.mother_ssn = request.json.get('mother_ssn')
    student.address = request.json.get('address')
    
    user.student_info = student
    db.session.add(user)
    db.session.add(student)
    db.session.commit()
    return jsonify({'user': user.as_dict()}), 201

@app.route('/api/student_infos/<int:id>', methods=['PUT'])
@multi_auth.login_required
def student_update(id):
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

    if user.student_info:
        student_info = user.student_info
    else:
        student_info = StudentInfo()
        student_info.user_id = user.id
        user.role_new('agit_student')
        user.student_info = student_info

    student_info.student_id = request.json.get('student_id')
    student_info.gender = request.json.get('gender')
    student_info.ssn = request.json.get('ssn')
    student_info.father_name = request.json.get('father_name')
    student_info.father_ssn = request.json.get('father_ssn')
    student_info.mother_name = request.json.get('mother_name')
    student_info.mother_ssn = request.json.get('mother_ssn')
    student_info.address = request.json.get('address')

    db.session.add(user)
    db.session.add(student_info)
    db.session.commit()
    return jsonify({'user': user.as_dict()})

@app.route('/api/student_infos/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def student_del(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'result': True})


##################################################
# class
##################################################
@app.route('/api/classes/major_categories')
def get_classes_major_categories():
    categories = Class.major_categories()
    return jsonify(categories)

@app.route('/api/classes', methods=['GET'])
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
    offset = (page - 1) * per_page
    classes = Class.query
    query = literal_eval(request.args.get('query'))
    
    if 'major_category' in query:
        classes = classes.filter_by(major_category=query['major_category'])
    if 'id' in query:
        classes = classes.filter_by(id=query['id'])
    if 'teacher_id' in query:
        classes = classes.filter_by(teacher_id=query['teacher_id'])
    if 'minor_category' in query:
        classes = classes.filter_by(minor_category=query['minor_category'])
    #if 'teacher_id' in request.args:
    #    classes = classes.filter_by(teacher_id=request.args['teacher_id'])

    classes = classes.all()
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

    teacher_id = request.json.get('teacher_id')
    teacher = User.query.filter_by(id=teacher_id).first()
    if not teacher:
        abort(404)
    
    class_.teacher_id = teacher.id
    class_.teacher = teacher
    class_.title = request.json.get('title')
    class_.major_category = request.json.get('major_category')
    class_.minor_category = request.json.get('minor_category')
    class_.year = int(request.json.get('year'))
    class_.semester = int(request.json.get('semester'))
    class_.time_slot = request.json.get('time_slot')
    class_.audience = request.json.get('audience')
    class_.background = request.json.get('background')
    class_.content = request.json.get('content')
    class_.teacher = teacher
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
    class_.major_category = request.json.get('major_category', class_.category)
    class_.minor_category = request.json.get('minor_category', class_.category)
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
@multi_auth.login_required
def enrollment_all():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    offset = (page - 1) * per_page
    query = literal_eval(request.args.get('query'))
    enrollments = Enrollment.query
    if 'class_id' in query:
        enrollments = enrollments.filter_by(class_id=query['class_id'])
    if 'student_id' in query:
        enrollments = enrollments.filter_by(student_id=query['student_id'])
    enrollments = enrollments.all()
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
@multi_auth.login_required
def enrollment_new():
    if not request.json:
        abort(400)

    user = g.user
    if not user:
        abort(400)

    enrollment = Enrollment()
    print(enrollment.required_columns())
    for column in enrollment.required_columns():
        if column not in request.json:
            abort(400)

    enrollment.class_id = request.json.get('class_id')
    enrollment.student_id = request.json.get('student_id', user.id)
    enrollment.approval = False
    enrollment.student = User.query.filter_by(id = enrollment.student_id).first()
    class_ = Class.query.filter_by(id = enrollment.class_id).first()
    class_.students.append(enrollment)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'enrollment': enrollment.as_dict()}), 201

@app.route('/api/enrollments/<int:class_id>/<int:student_id>', methods=['GET'])
@multi_auth.login_required
def enrollment_get(class_id, student_id):
    enrollment = Enrollment.query.filter_by(class_id = class_id, student_id = student_id).first()
    if not enrollment:
        abort(404)
    enrollmentdict = enrollment.as_dict()
    return jsonify(enrollmentdict)

@app.route('/api/enrollments/<int:class_id>/<int:student_id>', methods=['PUT'])
@multi_auth.login_required
def enrollment_update(class_id, student_id):
    if not request.json:
        abort(400)
    enrollment = Enrollment.query.filter_by(class_id = class_id, student_id = student_id).first()
    if not enrollment:
        abort(404)

    approval = request.json.get('approval', False)
    
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'enrollment': enrollment.as_dict()})

@app.route('/api/enrollments/<int:class_id>/<int:student_id>', methods=['DELETE'])
@multi_auth.login_required
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
@multi_auth.login_required
def post_all():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    offset = (page - 1) * per_page
    query = literal_eval(request.args.get('query'))

    posts = Post.query
    if 'major_category' in query:
        posts = posts.filter_by(major_category=query['major_category'])
    if 'minor_category' in query:
        posts = posts.filter_by(minor_category=query['minor_category'])
    if 'class_id' in query:
        posts = posts.filter_by(class_id=query['class_id'])
    posts = posts.all()
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
@multi_auth.login_required
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

    properties = request.json.get('properties', [])
    for prop in properties:
        post.properties_new(prop)
    post.title = request.json.get('title')
    post.body = request.json.get('body')
    class_id = request.json.get('class_id', None)
    if class_id:
        post.class_id = class_id
        post.class_ = Class.query.filter_by(id = class_id).first()

    author = User.query.filter_by(id = post.author_id).first()
    post.author = author
    db.session.add(post)
    db.session.commit()
    return jsonify({'post': post.as_dict()}), 201

@app.route('/api/posts/<int:id>', methods=['GET'])
@multi_auth.login_required
def post_get(id):
    post = Post.query.get(id)
    if not post:
        abort(404)
    postdict = post.as_dict()
    return jsonify(postdict)

@app.route('/api/posts/<int:id>', methods=['PUT'])
@multi_auth.login_required
def post_update(id):
    if not request.json:
        abort(400)
    post = Post.query.get(id)
    if not post:
        abort(404)

    post.major_category = request.json.get('major_category', post.major_category)
    post.minor_category = request.json.get('minor_category', post.minor_category)
    post.properties = json.dumps(request.json.get('properties', post.properties))
    post.title = request.json.get('title', post.title)
    post.body = request.json.get('body', post.body)

    properties = request.json.get('properties', post.properties)
    post.properties = '[]'
    if properties is None:
        properties = []
    for prop in properties:
        post.properties_new(prop)

    db.session.add(post)
    db.session.commit()
    return jsonify({'post': post.as_dict()})

@app.route('/api/posts/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def post_del(id):
    post = Post.query.filter_by(id = id).first()
    if not post:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'result': True})

##################################################
# attendance
##################################################
@app.route('/api/attendances/categories')
def get_attendances_categories():
    categories = Attendance.categories()
    return jsonify(categories)

@app.route('/api/attendances', methods=['GET'])
@multi_auth.login_required
def attendance_all():
    attendances = Attendance.query
    if 'category' in request.args:
        attendances = attendances.filter_by(category=request.args['category'])
    if 'class_id' in request.args:
        attendances = attendances.filter_by(class_id=request.args['class_id'])
    if 'student_id' in request.args:
        attendances = attendances.filter_by(student_id=request.args['student_id'])
    if 'date' in request.args:
        attendances = attendances.filter_by(date=date_from_str(request.args['date']))
    attendances = attendances.all()
    attendances_json = []
    for attendance in attendances:
        attendances_json.append(attendance.as_dict())
    return jsonify(attendances_json)

@app.route('/api/attendances', methods=['POST'])
@multi_auth.login_required
def attendance_new():
    if not request.json:
        abort(400)

    attendance = Attendance()
    print(attendance.required_columns())
    for column in attendance.required_columns():
        if column not in request.json:
            abort(400)

    attendance.class_id = request.json.get('class_id')
    attendance.student_id = request.json.get('student_id')
    attendance.date = date_from_str(request.json.get('date'))
    attendance.category = request.json.get('category')
    attendance.description = request.json.get('description')

    class_ = Class.query.filter_by(id = attendance.class_id).first()
    student = User.query.filter_by(id = attendance.student_id).first()
    attendance.class_ = class_
    attendance.student = student
    db.session.add(attendance)
    db.session.commit()
    return jsonify({'attendance': attendance.as_dict()}), 201

@app.route('/api/attendances/<int:id>', methods=['GET'])
@multi_auth.login_required
def attendance_get(id):
    attendance = Attendance.query.get(id)
    if not attendance:
        abort(404)
    attendancedict = attendance.as_dict()
    return jsonify(attendancedict)

@app.route('/api/attendances/<int:id>', methods=['PUT'])
@multi_auth.login_required
def attendance_update(id):
    if not request.json:
        abort(400)
    attendance = Attendance.query.get(id)
    if not attendance:
        abort(404)

    attendance.category = request.json.get('category')
    attendance.description = request.json.get('description', '')

    db.session.add(attendance)
    db.session.commit()
    return jsonify({'attendance': attendance.as_dict()})

@app.route('/api/attendances/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def attendance_del(id):
    attendance = Attendance.query.get(id)
    if not attendance:
        abort(404)
    db.session.delete(attendance)
    db.session.commit()
    return jsonify({'result': True})

##################################################
# payment 
##################################################
@app.route('/api/payments', methods=['GET'])
@multi_auth.login_required
def payment_all():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))
    offset = (page - 1) * per_page
    query = literal_eval(request.args.get('query'))
    payments = Payment.query
    if 'user_id' in query:
        payments = payments.filter_by(class_id=query['user_id'])
    if 'major_category' in query:
        payments = payments.filter_by(student_id=query['major_category'])
    payments = payments.all()
    payments_json = []
    for payment in payments:
        payments_json.append(payment.as_dict())
    result = {
        'currentPage': page,
        'lastPage': math.ceil(len(payments) / per_page),
        'perPage': per_page,
        'total': len(payments),
        'data': payments_json[offset:(offset + per_page)]
    }
    return jsonify(result)
        

@app.route('/api/payments', methods=['POST'])
@multi_auth.login_required
def payment_new():
    if not request.json:
        abort(400)

    user = g.user
    if not user:
        abort(400)

    payment = Payment()
    print(payment.required_columns())
    for column in payment.required_columns():
        if column not in request.json:
            abort(400)

    payment.user_id = request.json.get('user_id')
    payment.cost = request.json.get('cost')
    payment.major_category = request.json.get('major_category')
    payment.year = request.json.get('year')
    payment.semester = request.json.get('semester')
    payment.date = request.json.get('date')

    payment.user = User.query.filter_by(id = payment.user_id).first()
    db.session.add(payment)
    db.session.commit()
    return jsonify({'payment': payment.as_dict()}), 201

@app.route('/api/payments/<int:id>', methods=['PUT'])
@multi_auth.login_required
def payment_update(id):
    if not request.json:
        abort(400)
    payment = Payment.query.get(id)
    if not payment:
        abort(404)

    payment.cost = request.json.get('cost')
    payment.major_category = request.json.get('major_category')
    payment.year = request.json.get('year')
    payment.semester = request.json.get('semester')
    payment.date = request.json.get('date')
    
    db.session.add(payment)
    db.session.commit()
    return jsonify({'payment': payment.as_dict()})

@app.route('/api/payments/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def payment_del(id):
    payment = Payment.query.get(id)
    if not payment:
        abort(404)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/api/menu')
@multi_auth.login_required
def get_menu():
    user = g.user
    if not user:
        abort(404)

    menu = [
        { 'href': 'user_form', 'params': {'action':'update'}, 'text': '회원정보', 'icon': 'mdi-account' },
        { 'heading': '아지트' },
        { 'href': 'class', 'params': {'major_category':'agit'}, 'text': '수강신청', 'icon': 'mdi-plus' },
        { 'href': 'enrollment_student', 'params': {'major_category':'agit', 'id':user.id}, 'text': '수강과목', 'icon': 'mdi-pencil' },
    ]

    if 'agit_student' in user.role and 'agit_teacher' not in user.role and 'admin' not in user.role:
        menu.append({ 'href': 'agit_teacher_application_form', 'params': {}, 'text': '교사 신청', 'icon': 'mdi-teach' })
    
    if 'agit_teacher' in user.role:
        menu.append({ 'href': 'class_teacher', 'params': {'major_category':'agit', 'id':user.id}, 'text': '수업 관리', 'icon': 'mdi-clipboard-text' })
    
    if 'howcs_teacher' in user.role:
        menu.append({ 'heading': '하우학교'})
        menu.append({ 'href': 'teaching_classes', 'params': {'major_category':'howcs', 'id':user.id}, 'text': '수업 관리', 'icon': 'mdi-clipboard-text' })
    
    if 'admin' in user.role:
        menu.append({ 'heading': '관리자'})
        menu.append({ 'href': 'user', 'params': {}, 'text': '아지트 회원관리', 'icon': 'mdi-account-edit' })
        menu.append({ 'href': 'agit_teacher', 'params': {}, 'text': '아지트 교사관리', 'icon': 'mdi-account-plus' })
        menu.append({ 'href': 'payment', 'params': {}, 'text': '아지트 회비관리', 'icon': 'mdi-currency-krw' })
        menu.append({ 'href': 'student', 'params': {}, 'text': '하우학교 학생관리', 'icon': 'mdi-account-multiple' })
        menu.append({ 'href': 'howcs_teacher', 'params': {}, 'text': '하우학교 교사관리', 'icon': 'mdi-account-settings-variant' })
        menu.append({ 'href': 'class', 'params': {'major_category':'howcs'}, 'text': '하우학교 수업관리', 'icon': 'mdi-clipboard-text' })
    
    
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
