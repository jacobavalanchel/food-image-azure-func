import random
import re
import string

from flask import request, jsonify, Response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from passlib.hash import bcrypt


def error_msg(error_msg_text):
    return jsonify({
        "result": "error",
        "info": error_msg_text
    })


def init(app, db):
    def is_a_email_format(email):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(email_regex, email):
            return True
        else:
            return False

    @app.route("/create_all", methods=["POST"])
    def create_all():
        db.create_all()

    class Users(db.Model):
        user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        email = db.Column(db.String(64), unique=True, nullable=False)
        password = db.Column(db.String(128), unique=False, nullable=False)
        username = db.Column(db.String(50), unique=True, nullable=True)
        user_label = db.Column(db.String(128), unique=False, nullable=True)
        age = db.Column(db.Integer, unique=False, nullable=True)
        gender = db.Column(db.String(16), unique=False, nullable=True)

        def __repr__(self):
            return f"<User(user_id={self.user_id}, username='{self.username}', user_type='{self.user_type}')>"

        def to_dict(self):
            return {c.name: getattr(self, c.name) for c in self.__table__.columns}

        def verify_password(self, password):
            """校验密码"""
            return bcrypt.verify(password, self.password)

        def set_password(self, password):
            """密码加密"""
            self.password = bcrypt.hash(password)

    @app.route("/user/list_all", methods=["POST"])
    def user_list():
        # users = db.session.execute(db.select(User).order_by(User.username)).scalars()
        users = Users.query.all()
        users_list = []
        for user in users:
            users_list.append(user.to_dict())
        return jsonify(users_list)

    # todo: complemented registration page
    @app.route("/user/register", methods=["POST"])
    def user_register():
        # 获取入参
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        # username = data.get("username")
        # is_admin = db.Column(db.Boolean, nullable=False, default=False)
        # is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
        # confirmed_on = db.Column(db.DateTime, nullable=True)

        # NOT_EMPTY check
        # if not email or not password or not username:
        if not email or not password:
            return jsonify({"result": "error", "info": "邮箱/密码/用户名不能为空"})
        if not is_a_email_format(email):
            return jsonify({"result": "error", "info": "邮箱格式不正确"})
        if Users.query.filter_by(email=email).first() is not None:
            print('email existed')
            return jsonify({"result": "error", "info": "邮箱已存在"})
        # if Users.query.filter_by(username=username).first() is not None:
        #     print('username existed')
        #     return jsonify({"code": 222, "info": "用户名已存在"})
        try:
            # todo: not randomised username
            gen_username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            user = Users(username=str(gen_username), email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            # log your exception in the way you want -> log to file, log as error with default logging, send by email. It's upon you
            db.session.rollback()
            db.session.flush()  # for resetting non-commited .add()
            return jsonify({
                "result": "error",
                "info": f"failed:{e.__str__()}"
            })
        return jsonify({
            "result": "success",
            "info": "registration success",
            "data": {"username": str(gen_username), "email": email}
        })

    @app.route("/user/login", methods=["POST"])
    def user_login():
        print(request.json)
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        the_user = Users.query.filter_by(email=email).first()
        if the_user is None:
            return error_msg("未找到对应user")
        if not the_user.verify_password(password):
            return jsonify({
                "result": "error",
                "info": f"login failed, password incorrect"
            })
        access_token = create_access_token(identity=email)
        return jsonify({
            "result": "success",
            "info": f"login success",
            "data": {"email": email},
            "access_token": access_token
        })

    @app.route("/user/delete", methods=["POST"])
    def user_delete():
        data = request.get_json()
        email = data.get("email")
        the_user = Users.query.filter_by(email=email).first()
        if the_user is None:
            return error_msg("未找到对应user")
        if isinstance(the_user, Response):
            return the_user
        db.session.delete(the_user)
        db.session.commit()
        return jsonify({
            "result": "success",
            "info": "deleting success",
            "data": {"email": email}
        })

    @app.route("/user/get_info", methods=["POST"])
    @jwt_required()
    def user_info():
        data = request.get_json()
        email = data.get("email")
        user_name = get_jwt_identity()
        the_user = Users.query.filter_by(username=user_name).first()
        print(the_user)
        if the_user is None:
            return error_msg("未找到对应user")
        if isinstance(the_user, Response):
            return the_user
        return jsonify({
            "result": "success",
            "info": "get info success",
            "email": the_user.email,
            "name": the_user.username,
            "user_label": the_user.user_label,
            "age": the_user.age,
            "gender": the_user.gender,
        })
