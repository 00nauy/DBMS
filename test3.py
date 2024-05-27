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
    def __init__(self, account, name, hash_password, credit):  
        self.account = account
        self.name = name
        self.hash_password = hash_password
        self.credit = credit
    
    def get_id(self):
        return self.account
  
    @staticmethod  
    def get_by_account(account):  
        db = pymysql.connect(host="localhost", user="root", password="egwegwegw612", database="library_system")  
        cursor = db.cursor()  
        sql_query = "SELECT user_name, password, credit FROM users WHERE user_account = %s"  
        values = (account,)  
        cursor.execute(sql_query, values)  
        result = cursor.fetchone()  
        db.close()  
        if result:  
            return User(account, result[0], result[1], result[2])  
        return None  
  
    def check_password(self, password):  
        return check_password_hash(self.hash_password, password)

@login_manager.user_loader  
def load_user(user_id):  
    return User.get_by_account(user_id)


# 登录页面  
@app.route('/', methods=['GET', 'POST'])  
@app.route('/login', methods=['GET', 'POST'])  
def login():  
    if request.method == 'POST':  
        account = request.form['account']  
        password = request.form['password']  
        user = User.get_by_account(account)  
        if user is None or not user.check_password(password):  
            flash("用户名或密码有误！", 'error')  
            return redirect(url_for('login'))  
        login_user(user)  
        return redirect(url_for('index'))
    return render_template('login.html')  

#注册页面
@app.route('/register', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        if password == repassword:
            db = pymysql.connect(host="localhost", user="root", password="egwegwegw612", database="library_system")
            cursor = db.cursor()
            hashed_password = generate_password_hash(password)
            sql_query = "INSERT INTO users (user_name, password, credit) VALUES (%s, %s, %s)"
            values = (name, hashed_password, 300) 
            cursor.execute(sql_query, values)

            sql_query = "SELECT MAX(user_account) FROM users"
            cursor.execute(sql_query)
            result = cursor.fetchone()
            db.commit()  
            db.close() 
            return '注册成功！你的用户号是{}。'.format(result[0])
        else:
            return '两次密码不一致'
    return render_template('regist.html')

# 登出页面  
@app.route('/logout')  
@login_required  
def logout():  
    logout_user()  
    return redirect(url_for('login')) 

#主页
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == "GET":
        return render_template('index.html', username = current_user.name)

#个人信息页
@app.route('/personal_info', methods=['GET', 'POST'])
@login_required
def ps_info():
    if request.method == "GET":
        return render_template('personal_info.html', userid = current_user.account, 
        username = current_user.name, usercredit = current_user.credit)

#借阅信息页
@app.route('/borrow_info', methods=['GET', 'POST'])
@login_required
def br_info():
    if request.method == "GET":
        db = pymysql.connect(host="localhost", user="root", password="egwegwegw612", database="library_system")
        cursor = db.cursor()
        sql_query = "SELECT book_id, start_time, end_ddl FROM borrow_info WHERE user_account = %s"
        values = (current_user.account,)  
        cursor.execute(sql_query, values)  
        result = cursor.fetchall()
        info1 = '无借阅记录!';info2 = '无借阅记录!';info3 = '无借阅记录!'
        if (len(result)>=1):
            info1 = '书号：{} 用户号：{} 开始时间：{} 归还期限：{}'.format(result[0][0],current_user.account,result[0][1],result[0][2])
        if (len(result)>=2):
            info2 = '书号：{} 用户号：{} 开始时间：{} 归还期限：{}'.format(result[1][0],current_user.account,result[1][1],result[1][2])
        if (len(result)>=3):
            info3 = '书号：{} 用户号：{} 开始时间：{} 归还期限：{}'.format(result[2][0],current_user.account,result[2][1],result[2][2])
        db.close()
        return render_template('borrow_info.html', info1=info1,info2=info2,info3=info3)

#借书信息页
@app.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow():
    if request.method == "GET":
        return render_template('personal_info.html', userid = current_user.account, 
        username = current_user.name, usercredit = current_user.credit)

if __name__ == '__main__':
    app.run(debug=True)