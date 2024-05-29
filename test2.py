import pymysql
from flask import Flask
from flask import request, render_template, redirect, url_for, flash
from flask_login import UserMixin, login_user, login_required, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'abcdefg'

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message = '请先登录！'
login_manager.init_app(app=app)

class User(UserMixin):  
    def __init__(self, account, name, password, credit):  
        self.id = account
        self.name = name
        self.credit = credit
        self.password = password
  
    @staticmethod  
    def get_by_account(account):  
        db = pymysql.connect(host="localhost", user="root", password="a", database="library_system")  
        cursor = db.cursor()  
        sql_query = "SELECT user_name, password, credit FROM users WHERE user_account = %s"  
        values = (account,)  
        cursor.execute(sql_query, values)  
        result = cursor.fetchone()  
        db.close()  
        if result:  
            return User(account, result[0], result[1], result[2])  
        return None  
  
    # @property  
    # def password(self):  
    #     raise AttributeError('password is not a readable attribute')  
  
    # @password.setter  
    # def password(self, password):  
    #     self.password_hash = generate_password_hash(password)  
  
    # def check_password(self, password):  
    #     return check_password_hash(self.password_hash, password)

@login_manager.user_loader  
def load_user(user_id):  
    return User.get_by_account(user_id)



#登录页面
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        db = pymysql.connect(host="localhost", user="root", password="a", database="library_system")
        cursor = db.cursor()
        sql_query = "SELECT password FROM users WHERE user_account = %s"  
        values = (account,)  
        cursor.execute(sql_query, values)  
        result = cursor.fetchone()  
        if result is not None:  
            stored_password = result[0]  
            if password == stored_password:
                print(f"User '{account}' logged in successfully!")  
                return redirect(url_for('index'))
            else:  
                flash("Invalid password!",'error')
                return redirect(url_for('login'))
    return render_template('login.html')

#注册页面
@app.route('/register', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        if password == repassword:
            db = pymysql.connect(host="localhost", user="root", password="a", database="library_system")
            cursor = db.cursor()
            # hashed_password = generate_password_hash(password)
            sql_query = "INSERT INTO users (user_name, password, credit) VALUES (%s, %s, %s)"
            values = (name, password, 300) 
            cursor.execute(sql_query, values)  
            db.commit()  
            return '注册成功'
        else:
            return '两次密码不一致'
    return render_template('regist.html')

#主页
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)