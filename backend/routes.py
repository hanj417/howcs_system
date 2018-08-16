import math
import os
from flask import Flask, render_template, jsonify, abort, request, g, url_for
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from flask_mail import Message
from backend import app
from backend import mail
from backend.models import *
from flask import make_response
from flask import redirect
from flask import send_from_directory
from werkzeug.utils import secure_filename
from ast import literal_eval
from datetime import datetime, date, timedelta

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)

def mail_to_admin():
    msg = Message("Hello",
                  recipients=["hanj417@gmail.com"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    mail.send(msg)


#######################################
# authentication
#######################################
@basic_auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    print(user.name)
    return True

@token_auth.verify_token
def verify_token(username_or_token):
    user = User.verify_auth_token(username_or_token)
    if not user:
        return False
    g.user = user
    return True

@app.route('/api/login', methods=['GET'])
@multi_auth.login_required
def login_get():
    user = g.user
    if not user:
        return False
    user_info = g.user.as_dict()
    return jsonify({'user': user_info})

@app.route('/api/login', methods=['POST'])
@multi_auth.login_required
def login():
    token = g.user.generate_auth_token(3600)
    user_info = g.user.as_dict()
    return jsonify({'user': user_info, 'token': token.decode('ascii')})

@app.route('/api/token')
@multi_auth.login_required
def auth_token_new():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

#######################################
# uploads 
#######################################
ALLOWED_EXTENSIONS = set(['xlsx', 'pptx', 'docx', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('uploaded_file', filename=filename))

##################################################
# user 
##################################################
@app.route('/api/users', methods=['GET'])
@multi_auth.login_required
def user_all():
    user = g.user
    if not user.check_priv('user'):
        abort(403)

    users = User.query
    if 'name' in request.args:
        users = users.filter_by(name=request.args['name'])
    if 'role' in request.args:
        users = users.filter(User.role.contains(request.args['role']))
    users = users.all()
    users_json = []
    for user in users:
        users_json.append(user.as_dict())
    return jsonify(users_json)

@app.route('/api/users', methods=['POST'])
def user_new():
    # login not required
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        abort(400)

    username = request.json.get('username')
    if User.exist(username):
        abort(400)

    user = User(username=username)
    user.password = user.hash_password(request.json.get('password'))
    user.role_new(User.default_role())
    user.name = request.json.get('name', '')
    user.email = request.json.get('email', '')
    user.phone = request.json.get('phone', '')
    user.church = request.json.get('church', '')
    user.school = request.json.get('school', '')
    user.birthday_is(request.json.get('birthday'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'user': user.as_dict()}), 201

@app.route('/api/users/<int:id>', methods=['GET'])
@multi_auth.login_required
def user_get(id):
    current_user = g.user
    if not current_user.check_priv('user') and current_user.id != id:
        abort(403)
    user = User.query.get(id)
    if not user:
        abort(404)
    return jsonify(user.as_dict())

@app.route('/api/users/<int:id>', methods=['PUT'])
@multi_auth.login_required
def user_update(id):
    current_user = g.user
    if not current_user.check_priv('user_update') and current_user.id != id:
        abort(403)
    user = User.query.get(id)
    if not user:
        abort(404)
    if not request.json:
        abort(400)

    #FIXME: we do not allow username update
    #user.username = request.json.get('username')
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
    current_user = g.user
    if not current_user.check_priv('user_del'):
        abort(403)
    user = User.query.get(id)
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'result': True})

##################################################
# privileges
##################################################
@app.route('/api/privileges', methods=['GET'])
@multi_auth.login_required
def privilege_all():
    user = g.user
    if not user:
        abort(403)
    if 'priv' not in request.args:
        # admin requests all privs
        if 'admin' not in user.role:
            abort(403)
        if 'role' not in request.args:
            abort(400)
        privs = Privilege.query.filter_by(name=request.args['role']).first()
        if privs is None:
            abort(400)
        priv_json = []
        priv_dict = privs.as_dict()
        for category in Privilege.categories():
            c = {}
            c['category'] = category
            c['view'] = priv_dict[category]
            c['new'] = priv_dict[category+'_new']
            c['update'] = priv_dict[category+'_update']
            c['del'] = priv_dict[category+'_del']
            priv_json.append(c)
        return jsonify(priv_json)
    return jsonify(user.check_priv(request.args['priv']))

@app.route('/api/privileges/roles', methods=['GET'])
@multi_auth.login_required
def privilege_role_all():
    user = g.user
    if not user:
        abort(403)
    if 'admin' not in user.role:
        abort(403)
    privs = Privilege.query.all()
    role_json = []
    for priv in privs:
        role_json.append({'id':priv.id, 'name':priv.name, 'label':priv.label})
    return jsonify(role_json)

@app.route('/api/privileges', methods=['POST'])
@multi_auth.login_required
def privilege_new():
    user = g.user
    if not user:
        abort(401)
    if not user.role_check('admin'):
        abort(403)
    if not request.json or 'name' not in request.json or 'label' not in request.json:
        abort(400)

    privilege = Privilege()
    privilege.name = request.json.get('name')
    privilege.label = request.json.get('label')
    if privilege.name == '' or Privilege.exist(privilege.name):
        abort(400)
    if privilege.label == '' or Privilege.exist(privilege.label):
        abort(400)
    db.session.add(privilege)
    db.session.commit()
    return jsonify({'privilege': privilege.as_dict()}), 201

@app.route('/api/privileges/<int:id>', methods=['GET'])
@multi_auth.login_required
def privilege_get(id):
    user = g.user
    if not user:
        abort(401)
    if not user.role_check('admin'):
        abort(403)
    privilege = Privilege.query.get(id)
    if not privilege:
        abort(404)
    #return jsonify(privilege.as_dict())
    priv_json = []
    priv_dict = privilege.as_dict()
    for category in Privilege.categories():
        c = {}
        c['category'] = category
        c['view'] = priv_dict[category]
        c['new'] = priv_dict[category+'_new']
        c['update'] = priv_dict[category+'_update']
        c['del'] = priv_dict[category+'_del']
        priv_json.append(c)
    return jsonify(priv_json)

@app.route('/api/privileges/<int:id>', methods=['PUT'])
@multi_auth.login_required
def privilege_update(id):
    user = g.user
    if not user:
        abort(401)
    if not user.role_check('admin'):
        abort(403)
    if not request.json:
        abort(400)
    privilege = Privilege.query.get(id)
    if not privilege:
        abort(404)

    privilege.name = request.json.get('name', privilege.name)
    privilege.label = request.json.get('label', privilege.label)
    privilege.user = request.json.get('user', privilege.user)
    privilege.user_new = request.json.get('user_new', privilege.user)
    privilege.user_update = request.json.get('user_update', privilege.user)
    privilege.user_del = request.json.get('user_del', privilege.user)
    privilege.student = request.json.get('student', privilege.student)
    privilege.student_new = request.json.get('student_new', privilege.student_new)
    privilege.student_update = request.json.get('student_update', privilege.student_update)
    privilege.student_del = request.json.get('student_del', privilege.student_del)
    privilege.howcs_teacher = request.json.get('howcs_teacher', privilege.howcs_teacher)
    privilege.howcs_teacher_new = request.json.get('howcs_teacher_new', privilege.howcs_teacher_new)
    privilege.howcs_teacher_update = request.json.get('howcs_teacher_update', privilege.howcs_teacher_update)
    privilege.howcs_teacher_del = request.json.get('howcs_teacher_del', privilege.howcs_teacher_del)
    privilege.howcs_class = request.json.get('howcs_class', privilege.howcs_class)
    privilege.howcs_class_new = request.json.get('howcs_class_new', privilege.howcs_class_new)
    privilege.howcs_class_update = request.json.get('howcs_class_update', privilege.howcs_class_update)
    privilege.howcs_class_del = request.json.get('howcs_class_del', privilege.howcs_class_del)
    privilege.howcs_enrollment = request.json.get('howcs_enrollment', privilege.howcs_enrollment)
    privilege.howcs_enrollment_new = request.json.get('howcs_enrollment_new', privilege.howcs_enrollment_new)
    privilege.howcs_enrollment_update = request.json.get('howcs_enrollment_update', privilege.howcs_enrollment_update)
    privilege.howcs_enrollment_del = request.json.get('howcs_enrollment_del', privilege.howcs_enrollment_del)
    privilege.howcs_attendance = request.json.get('howcs_attendance', privilege.howcs_attendance)
    privilege.howcs_attendance_new = request.json.get('howcs_attendance_new', privilege.howcs_attendance_new)
    privilege.howcs_attendance_update = request.json.get('howcs_attendance_update', privilege.howcs_attendance_update)
    privilege.howcs_attendance_del = request.json.get('howcs_attendance_del', privilege.howcs_attendance_del)
    privilege.howcs_student_health_record = request.json.get('howcs_student_health_record', privilege.howcs_student_health_record)
    privilege.howcs_student_health_record_new = request.json.get('howcs_student_health_record_new', privilege.howcs_student_health_record_new)
    privilege.howcs_student_health_record_update = request.json.get('howcs_student_health_record_update', privilege.howcs_student_health_record_update)
    privilege.howcs_student_health_record_del = request.json.get('howcs_student_health_record_del', privilege.howcs_student_health_record_del)
    privilege.howcs_student_fruit_record = request.json.get('howcs_student_fruit_record', privilege.howcs_student_fruit_record)
    privilege.howcs_student_fruit_record_new = request.json.get('howcs_student_fruit_record_new', privilege.howcs_student_fruit_record_new)
    privilege.howcs_student_fruit_record_update = request.json.get('howcs_student_fruit_record_update', privilege.howcs_student_fruit_record_update)
    privilege.howcs_student_fruit_record_del = request.json.get('howcs_student_fruit_record_del', privilege.howcs_student_fruit_record_del)
    privilege.howcs_post = request.json.get('howcs_post', privilege.howcs_post)
    privilege.howcs_post_new = request.json.get('howcs_post_new', privilege.howcs_post_new)
    privilege.howcs_post_update = request.json.get('howcs_post_update', privilege.howcs_post_update)
    privilege.howcs_post_del = request.json.get('howcs_post_del', privilege.howcs_post_del)
    '''
    privilege.agit_class = request.json.get('agit_class', privilege.agit_class)
    privilege.agit_class_new = request.json.get('agit_class_new', privilege.agit_class_new)
    privilege.agit_class_update = request.json.get('agit_class_update', privilege.agit_class_update)
    privilege.agit_class_del = request.json.get('agit_class_del', privilege.agit_class_del)
    privilege.agit_teacher = request.json.get('agit_teacher', privilege.agit_teacher)
    privilege.agit_teacher_new = request.json.get('agit_teacher_new', privilege.agit_teacher_new)
    privilege.agit_teacher_update = request.json.get('agit_teacher_update', privilege.agit_teacher_update)
    privilege.agit_teacher_del = request.json.get('agit_teacher_del', privilege.agit_teacher_del)
    privilege.agit_enrollment = request.json.get('agit_enrollment', privilege.agit_enrollment)
    privilege.agit_enrollment_new = request.json.get('agit_enrollment_new', privilege.agit_enrollment_new)
    privilege.agit_enrollment_update = request.json.get('agit_enrollment_update', privilege.agit_enrollment_update)
    privilege.agit_enrollment_del = request.json.get('agit_enrollment_del', privilege.agit_enrollment_del)
    privilege.agit_attendance = request.json.get('agit_attendance', privilege.agit_attendance)
    privilege.agit_attendance_new = request.json.get('agit_attendance_new', privilege.agit_attendance_new)
    privilege.agit_attendance_update = request.json.get('agit_attendance_update', privilege.agit_attendance_update)
    privilege.agit_attendance_del = request.json.get('agit_attendance_del', privilege.agit_attendance_del)
    '''
    privilege.homepage_post = request.json.get('homepage_post', privilege.homepage_post)
    privilege.homepage_post_new = request.json.get('homepage_post_new', privilege.homepage_post_new)
    privilege.homepage_post_update = request.json.get('homepage_post_update', privilege.homepage_post_update)
    privilege.homepage_post_del = request.json.get('homepage_post_del', privilege.homepage_post_del)
    db.session.add(privilege)
    db.session.commit()
    return jsonify({'privilege': privilege.as_dict()})

@app.route('/api/privileges/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def privilege_del(id):
    user = g.user
    if not user:
        abort(401)
    if not user.role_check('admin'):
        abort(403)
    privilege = Privilege.query.get(id)
    if not privilege:
        abort(404)
    db.session.delete(privilege)
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
        abort(401)
    if not user.check_priv('agit_teacher'):
        abort(403)

    agit_teacher_infos = AgitTeacherInfo.query
    agit_teacher_infos = agit_teacher_infos.all()
    agit_teacher_infos_json = []
    for agit_teacher_info in agit_teacher_infos:
        agit_teacher_infos_json.append(agit_teacher_info.as_dict())
    return jsonify(agit_teacher_infos_json)

@app.route('/api/agit_teacher_infos', methods=['POST'])
@multi_auth.login_required
def agit_teacher_infos_new():
    user = g.user
    if not user:
        abort(401)
    if not user.check_priv('agit_teacher_new'):
        abort(403)
    if not request.json or not 'career' in request.json:
        abort(400)

    agit_teacher_info = AgitTeacherInfo()
    agit_teacher_info.user_id = user.id
    agit_teacher_info.career = request.json.get('career')
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
        abort(401)
    agit_teacher_info = AgitTeacherInfo.query.get(id)
    if not agit_teacher_info:
        abort(404)
    if not user.check_priv('agit_teacher_update') and agit_teacher_info.user_id != user.id:
        abort(403)
    if not request.json:
        abort(400)

    if user.check_priv('agit_teacher_update'):
        agit_teacher_info.approval = request.json.get('approval', agit_teacher_info.approval)
        if agit_teacher_info.approval == True:
            agit_teacher_info.user.role_new('agit_teacher')
        if agit_teacher_info.approval == False:
            agit_teacher_info.user.role_del('agit_teacher')
    agit_teacher_info.career = request.json.get('career', agit_teacher_info.career)
         
    db.session.add(agit_teacher_info)
    db.session.commit()
    return jsonify({'agit_teacher_info': agit_teacher_info.as_dict()})

@app.route('/api/agit_teacher_infos/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def agit_teacher_info_del(id):
    user = g.user
    if not user:
        abort(401)
    if not user.check_priv('agit_teacher_del'):
        abort(403)
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
        abort(401)
    if not user.check_priv('howcs_teacher'):
        abort(403)

    howcs_teacher_infos = HowcsTeacherInfo.query
    howcs_teacher_infos = howcs_teacher_infos.all()
    howcs_teacher_infos_json = []
    for howcs_teacher_info in howcs_teacher_infos:
        howcs_teacher_infos_json.append(howcs_teacher_info.as_dict())
    return jsonify(howcs_teacher_infos_json)

@app.route('/api/howcs_teacher_infos', methods=['POST'])
@multi_auth.login_required
def howcs_teacher_infos_new():
    user = g.user
    if not user:
        abort(401)
    if not user.check_priv('howcs_teacher_new'):
        abort(403)
    if not request.json or 'user_id' not in request.json:
        abort(400)
    user = User.query.filter_by(id = request.json.get('user_id')).first()
    if not user:
        abort(400)

    howcs_teacher_info = HowcsTeacherInfo()
    howcs_teacher_info.user_id = user.id
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
        abort(401)
    if not user.check_priv('howcs_teacher_update'):
        abort(403)
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
        abort(401)
    if not user.check_priv('howcs_teacher_del'):
        abort(403)
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
@multi_auth.login_required
def get_student_infos_all():
    user = g.user
    if not user:
        abort(401)
    if not user.check_priv('student'):
        abort(403)
    student_infos = StudentInfo.query.all()
    users = []
    for student_info in student_infos:
        users.append(student_info.user)
    users_json = []
    for user in users:
        if user:
            users_json.append(user.as_dict())
    return jsonify(users_json)

@app.route('/api/student_infos', methods=['POST'])
@multi_auth.login_required
def student_new():
    user = g.user
    if not user:
        abort(401)
    if not user.check_priv('student_new'):
        abort(403)
    if not request.json or not 'username' in request.json or not 'password' in request.json or not 'student_id' in request.json:
        abort(400)

    username = request.json.get('username')
    student_id = request.json.get('student_id')
    if User.exist(username):
        abort(400)
    if StudentInfo.query.filter_by(student_id=student_id).first() is not None:
        abort(400)

    user = User(username=username)
    user.password = user.hash_password(request.json.get('password'))
    user.role_new(User.default_role())
    user.role_new('howcs_student')
    user.name = request.json.get('name', '')
    user.email = request.json.get('email', '')
    user.phone = request.json.get('phone', '')
    user.church = request.json.get('church', '')
    user.school = request.json.get('school', '')
    user.birthday_is(request.json.get('birthday'))

    student = StudentInfo()
    student.user_id = user.id
    student.student_id = student_id
    student.gender = request.json.get('gender')
    student.rrn = request.json.get('rrn')
    student.father_name = request.json.get('father_name')
    student.father_rrn = request.json.get('father_rrn')
    student.mother_name = request.json.get('mother_name')
    student.mother_rrn = request.json.get('mother_rrn')
    student.address = request.json.get('address')
    
    user.student_info = student
    student_record = StudentRecord()
    student.student_record = student_record
    
    db.session.add(user)
    db.session.add(student)
    db.session.add(student_record)
    db.session.commit()
    return jsonify({'user': user.as_dict()}), 201

@app.route('/api/student_infos/<int:id>', methods=['PUT'])
@multi_auth.login_required
def student_update(id):
    user = g.user
    if not user:
        abort(401)
    if not user.check_priv('student_update'):
        abort(403)
    if not request.json:
        abort(400)

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
        user.role_new('howcs_student')
        user.student_info = student_info
        student_record = StudentRecord()
        student_info.student_record = student_record
        db.session.add(student_record)

    student_info.student_id = request.json.get('student_id', student_info.student_id)
    student_info.gender = request.json.get('gender', student_info.gender)
    student_info.rrn = request.json.get('rrn', student_info.rrn)
    student_info.father_name = request.json.get('father_name', student_info.father_name)
    student_info.father_rrn = request.json.get('father_rrn', student_info.father_rrn)
    student_info.mother_name = request.json.get('mother_name', student_info.mother_name)
    student_info.mother_rrn = request.json.get('mother_rrn', student_info.mother_rrn)
    student_info.address = request.json.get('address', student_info.address)

    db.session.add(user)
    db.session.add(student_info)
    db.session.commit()
    return jsonify({'user': user.as_dict()})

@app.route('/api/student_infos/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def student_del(id):
    user = g.user
    if not user:
        abort(401)
    if not user.check_priv('student_del'):
        abort(403)

    user = User.query.get(id)
    if not user:
        abort(404)
    if not user.student_info:
        abort(404)
    student_info = user.student_info
    db.session.delete(student_info)
    db.session.commit()
    return jsonify({'result': True})


##################################################
# class
##################################################
@app.route('/api/classes/categories')
def get_classes_major_categories():
    categories = Class.major_categories()
    return jsonify(categories)

@app.route('/api/classes/categories/<string:major_category>', methods=['GET'])
def get_classes_minor_categories(major_category):
    categories = Class.minor_categories()
    return jsonify(categories[major_category])


@app.route('/api/classes', methods=['GET'])
def class_all():
    classes = Class.query
    if 'major_category' in request.args:
        classes = classes.filter_by(major_category=request.args['major_category'])
    if 'minor_category' in request.args:
        classes = classes.filter_by(minor_category=request.args['minor_category'])
    if 'id' in request.args:
        classes = classes.filter_by(id=request.args['id'])
    if 'teacher_id' in request.args:
        classes = classes.filter_by(teacher_id=request.args['teacher_id'])
    classes = classes.all()
    classes_json = []
    for class_ in classes:
        classes_json.append(class_.as_dict())
    return jsonify(classes_json)

@app.route('/api/classes', methods=['POST'])
@multi_auth.login_required
def class_new():
    user = g.user
    if not request.json:
        abort(401)
    major_category = request.json.get('major_category')
    if not major_category:
        abort(400)
    if not user.check_priv(major_category + '_class_new'):
        abort(403)

    class_ = Class()
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
    class_.year = int(request.json.get('year', '2018'))
    class_.semester = request.json.get('semester', 'year')
    class_.time_slot = request.json.get('time_slot', '')
    class_.google_calendar = request.json.get('google_calendar', '')
    class_.audience = request.json.get('audience', '')
    class_.background = request.json.get('background', '')
    class_.content = json.dumps(request.json.get('content', '{}'))
    class_.teacher = teacher
    db.session.add(class_)
    db.session.commit()
    return jsonify({'class': class_.as_dict()}), 201

@app.route('/api/classes/<int:id>', methods=['GET'])
@multi_auth.login_required
def class_get(id):
    class_ = Class.query.get(id)
    if not class_:
        abort(404)
    class_dict = class_.as_dict()
    return jsonify(class_dict)

@app.route('/api/classes/agit/<int:id>', methods=['GET'])
def agit_class_get(id):
    class_ = Class.query.get(id)
    if not class_:
        abort(404)
    if class_.major_category != 'agit':
        abort(404)
    class_dict = class_.as_dict()
    return jsonify(class_dict)

@app.route('/api/classes/<int:id>', methods=['PUT'])
@multi_auth.login_required
def class_update(id):
    user = g.user
    if not request.json:
        abort(401)
    if not request.json:
        abort(400)
    major_category = request.json.get('major_category')
    if not major_category:
        abort(400)
    if not user.check_priv(major_category + '_class_update'):
        abort(403)
    class_ = Class.query.get(id)
    if not class_:
        abort(404)

    teacher_id = request.json.get('teacher_id', class_.teacher_id)
    teacher = User.query.filter_by(id=teacher_id).first()
    if not teacher:
        abort(404)
    
    class_.teacher_id = teacher.id
    class_.teacher = teacher
    class_.title = request.json.get('title', class_.title)
    class_.major_category = request.json.get('major_category', class_.major_category)
    class_.minor_category = request.json.get('minor_category', class_.minor_category)
    class_.year = int(request.json.get('year', class_.year))
    class_.semester = request.json.get('semester', class_.semester)
    class_.time_slot = request.json.get('time_slot', class_.time_slot)
    class_.google_calendar = request.json.get('google_calendar', class_.google_calendar)
    class_.audience = request.json.get('audience', class_.audience)
    class_.background = request.json.get('background', class_.background)
    class_.content = json.dumps(request.json.get('content', '{}'))
    class_.approval = request.json.get('approval', class_.approval)
    db.session.add(class_)
    db.session.commit()
    return jsonify({'class_': class_.as_dict()})

@app.route('/api/classes/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def class_del(id):
    user = g.user
    if not request.json:
        abort(401)
    if not request.json:
        abort(400)
    class_ = Class.query.get(id)
    if not class_:
        abort(404)
    major_category = class_.major_category
    if not major_category:
        abort(400)
    if not user.check_priv(major_category + '_class_del'):
        abort(403)
    db.session.delete(class_)
    db.session.commit()
    return jsonify({'result': True})


##################################################
# enrollment 
##################################################
@app.route('/api/enrollments', methods=['GET'])
@multi_auth.login_required
def enrollment_all():
    enrollments = Enrollment.query
    if 'class_id' in request.args:
        enrollments = enrollments.filter_by(class_id=request.args['class_id'])
    if 'student_id' in request.args:
        enrollments = enrollments.filter_by(student_id=request.args['student_id'])
    #enrollments = enrollments.order_by('subject_code asc')
    enrollments = enrollments.all()
    enrollments_json = []
    for enrollment in enrollments:
        if 'major_category' in request.args and enrollment.class_.major_category != request.args.get('major_category'):
            continue
        if 'minor_category' in request.args and enrollment.class_.minor_category != request.args.get('minor_category'):
            continue
        enrollments_json.append(enrollment.as_dict())
    return jsonify(enrollments_json)
        

@app.route('/api/enrollments', methods=['POST'])
@multi_auth.login_required
def enrollment_new():
    user = g.user
    if not user:
        abort(401)
    if not request.json:
        abort(400)

    enrollment = Enrollment()
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

@app.route('/api/enrollments/agit', methods=['POST'])
@multi_auth.login_required
def agit_enrollment_new():
    user = g.user
    if not user:
        abort(401)
    if not request.json:
        abort(400)

    class_id = request.json.get('class_id')
    student_id = user.id

    if Enrollment.query.filter_by(class_id = class_id, student_id = student_id).first():
        enrollment = Enrollment.query.filter_by(class_id = class_id, student_id = student_id).first()
        return jsonify({'enrollment': enrollment.as_dict()}), 201
        

    enrollment = Enrollment()
    for column in enrollment.required_columns():
        if column not in request.json:
            abort(400)

    enrollment.class_id = request.json.get('class_id')
    enrollment.student_id = user.id
    enrollment.approval = False
    enrollment.student = User.query.filter_by(id = enrollment.student_id).first()
    class_ = Class.query.filter_by(id = enrollment.class_id).first()
    class_.students.append(enrollment)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'enrollment': enrollment.as_dict()}), 201

@app.route('/api/enrollments/agit', methods=['POST'])
@multi_auth.login_required
def agit_enrollment_new():
    user = g.user
    if not user:
        abort(401)
    if not request.json:
        abort(400)
    class_id = request.json.get('class_id')
    student_id = user.id
    if Enrollment.query.filter_by(class_id = class_id, student_id = student_id).first():
        enrollment = Enrollment.query.filter_by(class_id = class_id, student_id = student_id).first()
        return jsonify({'enrollment': enrollment.as_dict()}), 201
        
    enrollment = Enrollment()
    for column in enrollment.required_columns():
        if column not in request.json:
            abort(400)
    enrollment.class_id = request.json.get('class_id')
    enrollment.student_id = user.id
    enrollment.approval = False
    enrollment.student = User.query.filter_by(id = enrollment.student_id).first()
    class_ = Class.query.filter_by(id = enrollment.class_id).first()
    class_.students.append(enrollment)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'enrollment': enrollment.as_dict()}), 201


@app.route('/api/enrollments/<int:id>', methods=['GET'])
@multi_auth.login_required
def enrollment_get(id):
    enrollment = Enrollment.query.filter_by(id = id).first()
    if not enrollment:
        abort(404)
    enrollmentdict = enrollment.as_dict()
    return jsonify(enrollmentdict)

@app.route('/api/enrollments/<int:class_id>/<int:student_id>', methods=['GET'])
@multi_auth.login_required
def enrollment_get_by_class_student(class_id, student_id):
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
@app.route('/api/posts/categories')
def get_posts_major_categories():
    categories = Post.major_categories()
    return jsonify(categories)

@app.route('/api/posts/categories/<string:major_category>', methods=['GET'])
def get_posts_minor_categories(major_category):
    categories = Post.minor_categories()
    return jsonify(categories[major_category])

@app.route('/api/posts/properties')
def get_posts_properties():
    properties = Post.properties_list()
    return jsonify(properties)

@app.route('/api/posts', methods=['GET'])
@multi_auth.login_required
def post_all():
    posts = Post.query
    if 'major_category' in request.args:
        posts = posts.filter_by(major_category=request.args['major_category'])
    if 'minor_category' in request.args:
        posts = posts.filter_by(minor_category=request.args['minor_category'])
    if 'class_id' in request.args:
        posts = posts.filter_by(class_id=request.args['class_id'])
    if 'recent' in request.args:
        posts = posts.order_by('created_at desc').order_by('id desc').limit(int(request.args['recent']))
    posts = posts.order_by('created_at desc').order_by('id desc')
    posts = posts.all()
    posts_json = []
    for post in posts:
        posts_json.append(post.as_dict())
    return jsonify(posts_json)

@app.route('/api/posts/homepage', methods=['GET'])
def post_homepage_all():
    posts = Post.query
    posts = posts.filter_by(major_category='homepage')
    if 'minor_category' in request.args:
        posts = posts.filter_by(minor_category=request.args['minor_category'])
    if 'recent' in request.args:
        posts = posts.order_by('created_at desc').order_by('id desc').limit(int(request.args['recent']))
    else:
        posts = posts.order_by('created_at desc').order_by('id desc')
    posts = posts.all()
    posts_json = []
    for post in posts:
        posts_json.append(post.as_dict())
    return jsonify(posts_json)

@app.route('/api/posts', methods=['POST'])
@multi_auth.login_required
def post_new():
    if not request.json:
        abort(400)

    post = Post()
    for column in post.required_columns():
        if column not in request.json:
            abort(400)

    user = g.user
    if not user:
        abort(400)

    post.author_id = user.id
    post.major_category = request.json.get('major_category')
    post.minor_category = request.json.get('minor_category')

    properties = request.json.get('properties', [])
    for prop in properties:
        post.properties_new(prop)
    post.title = request.json.get('title')
    if 'created_at' in request.json:
        post.created_at_is(request.json.get('created_at'))
    post.body = request.json.get('body')
    post.files = json.dumps(request.json.get('files', '[]'))
    class_id = request.json.get('class_id', None)
    if class_id:
        post.class_id = class_id
        post.class_ = Class.query.filter_by(id = class_id).first()
    post.author = user
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

@app.route('/api/posts/homepage/<int:id>', methods=['GET'])
def post_homepage_get(id):
    post = Post.query.get(id)
    if not post:
        abort(404)
    if post.major_category != 'homepage':
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
    if 'created_at' in request.json:
        post.created_at_is(request.json.get('created_at', post.created_at))
    post.body = request.json.get('body', post.body)
    post.files = json.dumps(request.json.get('files', post.files))

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
        if 'days' in request.args:
            date_from = date_from_str(request.args['date'])
            days = int(request.args['days'])
            date_to = date_from
            while days > 0:
                date_to = date_to + timedelta(days=1)
                if date_to.weekday() < 1 or date_to.weekday() > 5:
                    continue
                days -= 1
            attendances = attendances.filter(Attendance.date.between(date_from, date_to))
        else:
            attendances = attendances.filter_by(date=date_from_str(request.args['date']))
    attendances = attendances.all()

    # class attendances
    if 'class_id' in request.args and 'student_id' not in request.args and 'date' in request.args and 'days' in request.args:
        class_ = Class.query.filter_by(id=request.args['class_id']).first()
        students = class_.students
        date_from = date_from_str(request.args['date'])
        days = int(request.args['days'])
        date_to = date_from
        while days > 0:
            date_to = date_to + timedelta(days=1)
            if date_to.weekday() < 1 or date_to.weekday() > 5:
                continue
            days -= 1
        attendances_json = {}
        name_dic = {}
        for student in students:
            attendances_json[student.student.name] = {}
            name_dic[student.student.name] = student.student.id
            
            for single_date in daterange(date_from, date_to):
                date_str = single_date.strftime("%Y-%m-%d")
                attendances_json[student.student.name][date_str] = {'category':Attendance.categories()[0], 'id':0}

        for attendance in attendances:
            attendances_json[attendance.student.name][attendance.date.strftime("%Y-%m-%d")] = {'category':attendance.category, 'id':attendance.id}
        attendances_json_list = []
        for attendance_name in attendances_json:
            attendance_row = {'id':name_dic[attendance_name], 'name': attendance_name}
            for attendance_date in attendances_json[attendance_name]:
                attendance_row[attendance_date] = attendances_json[attendance_name][attendance_date]
            attendances_json_list.append(attendance_row)
        return jsonify(attendances_json_list)

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
    payments = Payment.query
    if 'user_id' in request.args:
        payments = payments.filter_by(class_id=request.args['user_id'])
    if 'major_category' in request.args:
        payments = payments.filter_by(student_id=request.args['major_category'])
    payments = payments.all()
    payments_json = []
    for payment in payments:
        payments_json.append(payment.as_dict())
    return jsonify(payments_json)
        

@app.route('/api/payments', methods=['POST'])
@multi_auth.login_required
def payment_new():
    if not request.json:
        abort(400)

    user = g.user
    if not user:
        abort(400)

    payment = Payment()
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

##################################################
# student_record 
##################################################
@app.route('/api/student_records', methods=['get'])
@multi_auth.login_required
def student_record_all():
    student_records = StudentRecord.query
    if 'student_info_id' in request.args:
        student_records = student_records.filter_by(student_info_id=request.args['student_info_id'])
    student_records = student_records.all()
    student_records_json = []
    for student_record in student_records:
        student_records_json.append(student_record.as_dict())
    return jsonify(student_records_json)
        

@app.route('/api/student_records', methods=['POST'])
@multi_auth.login_required
def student_record_new():
    if not request.json:
        abort(400)

    user = g.user
    if not user:
        abort(400)

    if 'student_info_id' not in request.json:
        abort(404)

    student_record = StudentRecord()

    student_record.student_info_id = request.json.get('student_info_id')
    student_record.student_info = StudentInfo.query.filter_by(id = student_record.student_info_id).first()
    db.session.add(student_record)
    db.session.commit()
    return jsonify({'student_record': student_record.as_dict()}), 201

@app.route('/api/student_records/<int:id>', methods=['PUT'])
@multi_auth.login_required
def student_record_update(id):
    if not request.json:
        abort(400)
    student_record = StudentRecord.query.get(id)
    if not student_record:
        abort(404)

    db.session.add(student_record)
    db.session.commit()
    return jsonify({'student_record': student_record.as_dict()})

@app.route('/api/student_records/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def student_record_del(id):
    student_record = StudentRecord.query.get(id)
    if not student_record:
        abort(404)
    db.session.delete(student_record)
    db.session.commit()
    return jsonify({'result': True})

##################################################
# student_health_record 
##################################################
@app.route('/api/student_health_records', methods=['get'])
@multi_auth.login_required
def student_health_record_all():
    student_health_records = StudentHealthRecord.query
    if 'student_record_id' in request.args:
        student_health_records = student_health_records.filter_by(student_record_id=request.args['student_record_id'])
    student_health_records = student_health_records.all()
    student_health_records_json = []
    for student_health_record in student_health_records:
        student_health_records_json.append(student_health_record.as_dict())
    return jsonify(student_health_records_json)
        

@app.route('/api/student_health_records', methods=['POST'])
@multi_auth.login_required
def student_health_record_new():
    if not request.json:
        abort(400)

    user = g.user
    if not user:
        abort(400)

    if 'student_record_id' not in request.json:
        abort(404)

    student_health_record = StudentHealthRecord()

    student_health_record.student_record_id = request.json.get('student_record_id')
    student_health_record.date_is(request.json.get('date'))
    student_health_record.internal_medicine = request.json.get('internal_medicine', '')
    student_health_record.dental_clinic = request.json.get('dental_clinic', '')
    student_health_record.fluorine_coating = request.json.get('fluorine_coating', '')
    student_health_record.height = request.json.get('height', '')
    student_health_record.weight = request.json.get('weight', '')
    student_health_record.sight = request.json.get('sight', '')
    student_health_record.internal_medicine_content = request.json.get('internal_medicine_content', '')
    student_health_record.cavity = request.json.get('cavity', '')
    student_health_record.dental_clinic_content = request.json.get('dental_clinic_content', '')
    student_health_record.content = request.json.get('content', '')

    student_record = StudentRecord.query.filter_by(id = student_health_record.student_record_id).first()
    student_record.student_health_records.append(student_health_record)
    db.session.add(student_health_record)
    db.session.add(student_record)
    db.session.commit()
    return jsonify({'student_health_record': student_health_record.as_dict()}), 201

@app.route('/api/student_health_records/<int:id>', methods=['PUT'])
@multi_auth.login_required
def student_health_record_update(id):
    if not request.json:
        abort(400)
    student_health_record = StudentHealthRecord.query.get(id)
    if not student_health_record:
        abort(404)

    student_health_record.date_is(request.json.get('date'))
    student_health_record.internal_medicine = request.json.get('internal_medicine', student_health_record.internal_medicine)
    student_health_record.dental_clinic = request.json.get('dental_clinic', student_health_record.dental_clinic)
    student_health_record.fluorine_coating = request.json.get('fluorine_coating', student_health_record.fluorine_coating)
    student_health_record.height = request.json.get('height', student_health_record.height)
    student_health_record.weight = request.json.get('weight', student_health_record.weight)
    student_health_record.sight = request.json.get('sight', student_health_record.sight)
    student_health_record.internal_medicine_content = request.json.get('internal_medicine_content', student_health_record.internal_medicine_content)
    student_health_record.cavity = request.json.get('cavity', student_health_record.cavity)
    student_health_record.dental_clinic_content = request.json.get('dental_clinic_content', student_health_record.dental_clinic_content)
    student_health_record.content = request.json.get('content', student_health_record.content)
    
    db.session.add(student_health_record)
    db.session.commit()
    return jsonify({'student_health_record': student_health_record.as_dict()})

@app.route('/api/student_health_records/<int:id>', methods=['GET'])
@multi_auth.login_required
def student_health_record_get(id):
    student_health_record = StudentHealthRecord.query.get(id)
    if not student_health_record:
        abort(404)
    return jsonify(student_health_record.as_dict())

@app.route('/api/student_health_records/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def student_health_record_del(id):
    student_health_record = StudentHealthRecord.query.get(id)
    if not student_health_record:
        abort(404)
    db.session.delete(student_health_record)
    db.session.commit()
    return jsonify({'result': True})

##################################################
# student_fruit_record 
##################################################
@app.route('/api/student_fruit_records', methods=['get'])
@multi_auth.login_required
def student_fruit_record_all():
    user = g.user
    if not user:
        abort(400)

    student_fruit_records = StudentFruitRecord.query
    if 'enrollment_id' in request.args:
        student_fruit_records = student_fruit_records.filter_by(enrollment_id=request.args['enrollment_id'])
    student_fruit_records = student_fruit_records.all()
    if 'student_user_id' in request.args:
        if user.id != request.args['student_user_id']:
            abort(400)
        user  = User.query.filter_by(id=request.args['student_user_id']).first()
        student_fruit_records = user.student_info.student_record.student_annual_records[0].student_fruit_records
        student_fruit_records.sort(key=lambda x: x.subject_code)
    student_fruit_records_json = []
    for student_fruit_record in student_fruit_records:
        student_fruit_records_json.append(student_fruit_record.as_dict())
    return jsonify(student_fruit_records_json)
        

@app.route('/api/student_fruit_records', methods=['POST'])
@multi_auth.login_required
def student_fruit_record_new():
    if not request.json:
        abort(400)

    user = g.user
    if not user:
        abort(400)

    if 'enrollment_id' not in request.json:
        abort(404)

    enrollment_id = request.json.get('enrollment_id')
    enrollment = Enrollment.query.filter_by(id = enrollment_id).first()

    student_record = enrollment.student.student_info.student_record
    student_annual_records = student_record.student_annual_records
    if len(student_annual_records) == 0:
        student_annual_record = StudentAnnualRecord()
        student_annual_record.year = 2018
        student_annual_record.content = ''
        student_annual_records.append(student_annual_record)
    student_annual_record = student_annual_records[0]

    student_fruit_record = StudentFruitRecord()

    student_fruit_record.enrollment_id = enrollment_id
    student_fruit_record.student_annual_record_id = student_annual_record.id
    student_fruit_record.semester = request.json.get('semester', '')
    student_fruit_record.content = request.json.get('content', '')

    enrollment.student_fruit_records.append(student_fruit_record)
    student_annual_record.student_fruit_records.append(student_fruit_record)

    db.session.add(student_fruit_record)
    db.session.add(student_annual_record)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'student_fruit_record': student_fruit_record.as_dict()}), 201

@app.route('/api/student_fruit_records/<int:id>', methods=['PUT'])
@multi_auth.login_required
def student_fruit_record_update(id):
    if not request.json:
        abort(400)
    student_fruit_record = StudentFruitRecord.query.get(id)
    if not student_fruit_record:
        abort(404)

    student_fruit_record.semester = request.json.get('semester', student_fruit_record.semester)
    student_fruit_record.content = request.json.get('content', student_fruit_record.content)
    
    db.session.add(student_fruit_record)
    db.session.commit()
    return jsonify({'student_fruit_record': student_fruit_record.as_dict()})

@app.route('/api/student_fruit_records/<int:id>', methods=['GET'])
@multi_auth.login_required
def student_fruit_record_get(id):
    student_fruit_record = StudentFruitRecord.query.get(id)
    if not student_fruit_record:
        abort(404)
    return jsonify(student_fruit_record.as_dict())

@app.route('/api/student_fruit_records/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def student_fruit_record_del(id):
    student_fruit_record = StudentFruitRecord.query.get(id)
    if not student_fruit_record:
        abort(404)
    db.session.delete(student_fruit_record)
    db.session.commit()
    return jsonify({'result': True})



@app.route('/api/menu')
@multi_auth.login_required
def get_menu():
    user = g.user
    if not user:
        abort(404)

    menu = [
        { 'heading': '회원' },
        { 'href': 'user_form', 'params': {'action':'update'}, 'text': '회원정보', 'icon': 'account circle' },
        #{ 'href': '/hana/class', 'params': {'major_category':'agit'}, 'text': '수강신청', 'icon': 'plus' },
        #{ 'href': '/hana/enrollment_student', 'params': {'major_category':'agit', 'id':user.id}, 'text': '수강과목', 'icon': 'pencil' },
    ]
    '''
    roles = literal_eval(user.role)
    privs = {}
    for role in roles:
        privilege = Privilege.query.filter_by(name=role).first()
        if privilege is None:
            print("unknown role %s" % role)
            continue
        role_privs = privilege.as_dict()
        for priv in role_privs:
            if priv not in privs:
                privs[priv] = role_privs[priv]
            privs[priv] |= role_privs[priv]
    '''

    if 'agit_student' in user.role and 'agit_teacher' not in user.role and 'admin' not in user.role:
        menu.append({ 'heading': '아지트 학생'})
        menu.append({ 'href': 'enrollment_student_all', 'params': {'major_category':'agit', 'action':'post', 'id':user.id}, 'text': '공지사항', 'icon': 'sms failed' })
        menu.append({ 'href': 'agit_teacher_application', 'params': {}, 'text': '아지트 교사 신청', 'icon': 'account circle' })
    
    if 'agit_teacher' in user.role:
        menu.append({ 'heading': '아지트 교사'})
        menu.append({ 'href': 'agit_class_teacher', 'params': {'major_category':'agit', 'action':'edit', 'teacher_id':user.id}, 'text': '수업 목록', 'icon': 'class' })
        menu.append({ 'href': 'class_teacher', 'params': {'major_category':'agit', 'action':'enrollment', 'teacher_id':user.id}, 'text': '수강생 관리', 'icon': 'group add' })
        menu.append({ 'href': 'class_teacher', 'params': {'major_category':'agit', 'action':'post', 'teacher_id':user.id}, 'text': '공지사항', 'icon': 'sms failed' })
    
    if 'howcs_student' in user.role:
        menu.append({ 'heading': '하우학교 학생'})
        menu.append({ 'href': 'student_record', 'params': {'action':'view', 'id':user.id}, 'text': '인적사항', 'icon': 'assignment ind' })
        menu.append({ 'href': 'student_health_record', 'params': {'action':'view', 'id':user.id}, 'text': '건강기록부', 'icon': 'local hospital' })
        menu.append({ 'href': 'student_fruit_record', 'params': {'major_category':'howcs', 'minor_category':'subject', 'action':'view', 'id':user.id}, 'text': '열매 나누기', 'icon': 'event available' })
        #menu.append({ 'href': 'enrollment_student', 'params': {'major_category':'howcs', 'minor_category':'subject', 'action':'fruit', 'id':user.id}, 'text': '과목별 열매', 'icon': 'event available' })
        menu.append({ 'href': 'enrollment_student_all', 'params': {'major_category':'howcs', 'action':'post', 'id':user.id}, 'text': '공지사항', 'icon': 'sms failed' })
        menu.append({ 'href': 'enrollment_student', 'params': {'major_category':'howcs', 'minor_category':'class', 'action':'attendance', 'id':user.id}, 'text': '출결 관리', 'icon': 'event available' })
        menu.append({ 'href': 'enrollment_student', 'params': {'major_category':'howcs', 'minor_category':'parent_school', 'action':'attendance', 'id':user.id}, 'text': '부모학교', 'icon': 'wc' })
        menu.append({ 'href': 'resource', 'params': {'major_category':'howcs', 'minor_category':'edu_resource'}, 'text': '교육자료실', 'icon': 'folder' })
        menu.append({ 'href': 'resource', 'params': {'major_category':'howcs', 'minor_category':'academic_resource'}, 'text': '교무자료실', 'icon': 'folder open' })
    
    if 'howcs_teacher' in user.role:
        menu.append({ 'heading': '하우학교 교사'})
        menu.append({ 'href': 'howcs_class_teacher', 'params': {'major_category':'howcs', 'minor_category':'subject', 'action':'edit', 'teacher_id':user.id}, 'text': '수업 목록', 'icon': 'class' })
        menu.append({ 'href': 'howcs_class_teacher', 'params': {'major_category':'howcs', 'minor_category':'class', 'action':'edit', 'teacher_id':user.id}, 'text': '학급 목록', 'icon': 'school' })
        menu.append({ 'href': 'howcs_class_teacher', 'params': {'major_category':'howcs', 'minor_category':'class', 'action':'attendance', 'teacher_id':user.id}, 'text': '출결 관리', 'icon': 'event available' })
        menu.append({ 'href': 'class_teacher', 'params': {'major_category':'howcs', 'action':'enrollment', 'teacher_id':user.id}, 'text': '수강생 관리', 'icon': 'group add' })
        menu.append({ 'href': 'class_teacher', 'params': {'major_category':'howcs', 'action':'post', 'teacher_id':user.id}, 'text': '공지사항', 'icon': 'sms failed' })
        menu.append({ 'href': 'class_teacher', 'params': {'major_category':'howcs', 'action':'student_health_record', 'teacher_id':user.id}, 'text': '건강 기록 관리', 'icon': 'local hospital' })
        #menu.append({ 'href': 'class_teacher', 'params': {'major_category':'howcs', 'action':'student_fruit_record', 'teacher_id':user.id}, 'text': '열매 기록 관리', 'icon': 'local hospital' })
        menu.append({ 'href': 'resource', 'params': {'major_category':'howcs', 'minor_category':'edu_resource'}, 'text': '교육자료실', 'icon': 'folder' })
        menu.append({ 'href': 'resource', 'params': {'major_category':'howcs', 'minor_category':'academic_resource'}, 'text': '교무자료실', 'icon': 'folder open' })
    
    if 'admin' in user.role:
        menu.append({ 'heading': '관리자'})
        menu.append({ 'href': 'post_admin', 'params': {}, 'text': '글쓰기', 'icon': 'note add' })
        menu.append({ 'href': 'user', 'params': {}, 'text': '아지트 회원관리', 'icon': 'people' })
        menu.append({ 'href': 'agit_teacher', 'params': {}, 'text': '아지트 교사관리', 'icon': 'person' })
        menu.append({ 'href': 'agit_class_admin', 'params': {'major_category':'agit', 'action':'edit'}, 'text': '아지트 수업관리', 'icon': 'class' })
        menu.append({ 'href': 'class_all', 'params': {'major_category':'agit', 'action':'enrollment'}, 'text': '아지트 수강관리', 'icon': 'group add' })
        #menu.append({ 'href': '/hana/payment', 'params': {}, 'text': '아지트 회비관리', 'icon': 'currency-krw' })
        menu.append({ 'href': 'student', 'params': {'action':'student_record'}, 'text': '하우학교 학생관리', 'icon': 'group add' })
        menu.append({ 'href': 'student', 'params': {'action':'student_health_record'}, 'text': '하우학교 학생 건강기록', 'icon': 'local hospital' })
        menu.append({ 'href': 'howcs_teacher', 'params': {}, 'text': '하우학교 교사관리', 'icon': 'person' })
        menu.append({ 'href': 'class_all', 'params': {'major_category':'howcs', 'action':'edit'}, 'text': '하우학교 수업관리', 'icon': 'class' })
        menu.append({ 'href': 'class_all', 'params': {'major_category':'howcs', 'action':'attendance'}, 'text': '하우학교 출결관리', 'icon': 'event available' })
        menu.append({ 'href': 'class_all', 'params': {'major_category':'howcs', 'action':'enrollment'}, 'text': '하우학교 수강관리', 'icon': 'group add' })
        menu.append({ 'href': 'role', 'params': {}, 'text': '권한 관리', 'icon': 'lock' })
        menu.append({ 'href': 'resource', 'params': {'major_category':'howcs', 'minor_category':'edu_resource'}, 'text': '교육자료실', 'icon': 'folder' })
        menu.append({ 'href': 'resource', 'params': {'major_category':'howcs', 'minor_category':'academic_resource'}, 'text': '교무자료실', 'icon': 'folder open' })
    return jsonify(menu)

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
