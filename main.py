import pymysql
from flask import Flask
from flask import request, render_template, redirect, url_for, flash, jsonify, abort
from flask_login import UserMixin, login_user, login_required, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash
import datetime
from user_base import User
from manager_base import Manager

app = Flask(__name__)
app.secret_key = 'abcdefg'

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message = '请先登录！'
login_manager.init_app(app=app)


@login_manager.user_loader  
def load_user(user_id):  
    if int(user_id) < 10000000:
        return User.get_by_account(user_id)
    else:
        return Manager.get_by_account(user_id)


#登录页面  
#对应模板文件为'login.html'
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
#对应模板文件为'regist.html'
@app.route('/register', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        if password == repassword:
            db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
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


#主页，当用户登录成功后，进入主页
#对应模板文件为'index.html'
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if not isinstance(current_user, User): 
        abort(403)
    if request.method == "GET":
        return render_template('index.html', username = current_user.name)


#登出页面，当用户或管理员在主页按下“退出登录”按钮时，将退出登录并跳转到登录页面。
@app.route('/logout')  
@login_required  
def logout():  
    logout_user()  
    return redirect(url_for('login')) 


#个人信息页，当用户在主页按下“查询个人信息”按钮时，跳转到个人信息页，展示用户的个人信息。
#对应模板文件为'personal_info.html'
@app.route('/personal_info', methods=['GET', 'POST'])
@login_required
def ps_info():
    if not isinstance(current_user, User): 
        abort(403)
    if request.method == "GET":
        return render_template('personal_info.html', userid = current_user.account, 
        username = current_user.name, usercredit = current_user.credit)


#借阅信息页，当用户在主页按下“查询借阅信息”按钮时，跳转到借阅信息页，展示用户的当前借阅。
#对应模板文件为'borrow_info.html'
@app.route('/borrow_info', methods=['GET', 'POST'])
@login_required
def br_info():
    if not isinstance(current_user, User): 
        abort(403)
    if request.method == "GET":
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
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


#借书页1，当用户在主页按下“借书”按钮时，跳转到借书页1，这个页面将向用户展示书籍列表。
#对应模板文件为'borrow.html'
@app.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow():
    if not isinstance(current_user, User): 
        abort(403)
    if request.method == "GET":
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        sql_query = "SELECT * FROM books"
        cursor.execute(sql_query)  
        result = cursor.fetchall()
        db.commit() 
        db.close()
        return render_template('borrow.html',result=result)


#借书页2，当用户在借书页1按下“借阅”按钮时，跳转到借书页2，用户在这个页面设置借阅时长。
#对应模板文件为'borrow2.html'
@app.route('/borrow2', methods=['GET', 'POST'])
@login_required
def borrow2():
    if not isinstance(current_user, User): 
        abort(403)
    if request.method == "POST":
        id = request.form.get('book_id')   
        numdays = request.form.get('number') 
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        #此处先进行检查，可能会出现已经成功进入选择日期页面，但由于没有及时完成选择，被下架或别人先借走了书的情况，需要排除之。
        sql_query0 = "SELECT * FROM books WHERE book_id = %s"
        values = (id,)
        cursor.execute(sql_query0, values) 
        result = cursor.fetchone()
        if result is None:
            db.close()
            return '此书籍已经被下架！'
        if result[7] == 1:
            db.close()
            return '此书籍已经被借阅！'

        #修改书籍信息表，设置为已经被借
        sql_query1 = "UPDATE books SET borrowed = 1 WHERE book_id = %s"
        cursor.execute(sql_query1, values)  

        #修改借阅信息表，增加一条记录
        sql_query2 = "INSERT INTO borrow_info (book_id, user_account, start_time, end_ddl) VALUES (%s, %s, %s, %s)"
        current_date = datetime.date.today()
        end_date = current_date + datetime.timedelta(days=int(numdays))
        values2 = (id, current_user.account, current_date, end_date)
        cursor.execute(sql_query2, values2)  

        #修改用户信息表，扣除100借阅点数
        sql_query3 = "UPDATE users SET credit = credit-100 WHERE user_account = %s"
        values3 = (current_user.account,)
        cursor.execute(sql_query3, values3)  
        db.commit() 
        db.close()

        #返回借阅成功页面
        return '借阅成功！天数为{}天。'.format(numdays)
    else:
        #此处先进行检查，可能会出现“借阅”按钮亮起，但书已经被借走或下架的情况，需要排除之。
        book_id = request.args.get('book_id')
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        sql_query = "SELECT * FROM books WHERE book_id = %s"
        values = (book_id,)
        cursor.execute(sql_query, values)  
        result = cursor.fetchone()
        db.commit()
        db.close()
        if result is None:
            return '此书籍已经被下架！'
        if result[7] == 1:
            return '此书籍已经被借阅！'
        #此处检查借阅点数是否不足100，若不足100则无法借书
        if current_user.credit < 100:
            return '借阅点数不足！'
        #进入借书页2
        return render_template('borrow2.html', bookid = book_id)


#管理员登录页面  
#对应模板文件为'login_ad.html'
@app.route('/adlogin', methods=['GET', 'POST'])  
def adlogin():  
    if request.method == 'POST':  
        account = request.form['account']  
        password = request.form['password']  
        manager = Manager.get_by_account(account)  
        if manager is None or not manager.check_password(password):  
            flash("管理员名或密码有误！", 'error')  
            return redirect(url_for('login'))  
        login_user(manager)  
        return redirect(url_for('adindex'))
    return render_template('login_ad.html')  


#管理员注册页面
#对应模板文件为'regist_ad.html'
@app.route('/adregister', methods=['GET', 'POST'])
def adregist():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        if password == repassword:
            db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
            cursor = db.cursor()
            hashed_password = generate_password_hash(password)
            sql_query = "INSERT INTO manager (name, password) VALUES (%s, %s)"
            values = (name, hashed_password) 
            cursor.execute(sql_query, values)

            sql_query = "SELECT MAX(account) FROM manager"
            cursor.execute(sql_query)
            result = cursor.fetchone()
            db.commit()  
            db.close() 
            return '注册成功！你的管理员号是{}。'.format(result[0])
        else:
            return '两次密码不一致'
    return render_template('regist_ad.html')


#管理员主页，当管理员登录成功后，进入主页
#对应模板文件为'index_ad.html'
@app.route('/adindex', methods=['GET', 'POST'])
@login_required
def adindex():
    #若当前用户不是管理员，则禁止访问
    if not isinstance(current_user, Manager): 
        abort(403)
    if request.method == "GET":
        return render_template('index_ad.html', username = current_user.name)


#上架书籍页，当管理员在主页按下“上架书籍”按钮时，进入此页面，管理员在这个页面填写要上架的书籍信息。
#对应模板文件为'add_book.html'
@app.route('/addbook', methods=['GET', 'POST'])
@login_required
def addbook():
    #若当前用户不是管理员，则禁止访问
    if not isinstance(current_user, Manager): 
        abort(403)
    if request.method == "POST":
        #读取各项信息
        book_name = request.form['book_name']  
        class_category = request.form['class']  
        author = request.form['author']  
        publisher = request.form['publisher']  
        pubtime_str = request.form['pubtime']
        pubtime = datetime.datetime.strptime(pubtime_str, '%Y-%m-%d').date()
        current_date = datetime.date.today()
        values = (book_name,class_category,author,publisher,pubtime,current_date,0)

        #更新书籍信息表，新增一条记录
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        sql_query = "INSERT INTO books (book_name,class,author,publisher,pubtime,entertime,borrowed) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql_query, values)
        db.commit()  
        db.close() 
        return '操作成功！'
    return render_template('add_book.html')


#下架书籍页1，当管理员在主页按下“下架书籍”按钮时，跳转到下架书籍页1，这个页面将向管理员展示书籍列表。
#对应模板文件为'del_book.html'
@app.route('/delbook', methods=['GET', 'POST'])
@login_required
def delbook():
    if not isinstance(current_user, Manager): 
        abort(403)
    if request.method == "GET":
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        sql_query = "SELECT * FROM books"
        cursor.execute(sql_query)  
        result = cursor.fetchall()
        db.commit() 
        db.close()
        return render_template('del_book.html',result=result)


#当管理员在下架书籍页1按下“下架书籍”按钮时，进行下架操作并返回操作结果信息。
@app.route('/delbook2', methods=['GET', 'POST'])
@login_required
def delbook2():
    if not isinstance(current_user, Manager): 
        abort(403)
    #此处先进行检查，可能会出现“下架书籍”按钮亮起，但书已下架或已被借走的情况，需要排除之。
    book_id = request.args.get('book_id')
    db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
    cursor = db.cursor()
    sql_query = "SELECT * FROM books WHERE book_id = %s"
    values = (book_id,)
    cursor.execute(sql_query, values)  
    result = cursor.fetchone()
    if result is None:
        db.close()
        return '此书籍已经被下架！'
    if result[7] == 1:
        db.close()
        return '此书籍已经被借阅！'

    #更新书籍信息表，删除一条记录
    sql_query2 = "DELETE FROM books WHERE book_id = %s"
    cursor.execute(sql_query2, values) 
    db.commit()
    db.close()
    return '下架成功！'


#还书页面，当管理员在主页按下“还书”按钮时，跳转到此页面，管理员需要在此页面输入书号，若存在对应记录，则跳转到还书页面2。
#还书页面1对应模板文件为'return.html'，还书页面2对应模板文件为'return2.html'
@app.route('/return', methods=['GET', 'POST'])
@login_required
def returnbook():
    if not isinstance(current_user, Manager): 
        abort(403)
    if request.method == "POST":
        #读取信息
        book_id = request.form['id']  
        if not book_id.isdigit(): 
            return '请输入一个整数！'
        #在借阅信息表中根据书号查询借阅记录
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        sql_query = "SELECT * FROM borrow_info WHERE book_id = %s"
        values = (book_id,)
        cursor.execute(sql_query, values) 
        result = cursor.fetchone()
        if result is None:
            return '无借阅记录！'
        db.commit()
        db.close()
        return render_template('return2.html',result = result) 
    return render_template('return.html')


#当管理员在还书页面2按下“确认已还”时，进行还书操作并返回操作结果信息。
@app.route('/return2', methods=['GET', 'POST'])
@login_required
def returnbook2():
    if not isinstance(current_user, Manager): 
        abort(403)
    book_id = request.args.get('book_id')
    db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
    cursor = db.cursor()
    #可能存在“确认已还”按钮亮起，但书其实已经归还的情况，应该排除之
    #注：此处不完善！无法处理书已经被归还然后再被借走的特殊情况
    sql_query = "SELECT * FROM borrow_info WHERE book_id = %s"
    values = (book_id,)
    cursor.execute(sql_query, values)
    result = cursor.fetchone()
    if result is None:
        db.close()
        return '书已经被归还了！'

    #更新书籍信息表，将对应书籍设置为可借阅状态
    sql_query1 = "UPDATE books SET borrowed = 0 WHERE book_id = %s"
    values1 = (book_id,)
    cursor.execute(sql_query1, values1) 

    #更新用户信息表，如果按时归还，将增加100借阅点数
    sql_query2 = "SELECT * FROM borrow_info WHERE book_id = %s"
    values2 = (book_id,)
    cursor.execute(sql_query2, values2)
    result = cursor.fetchone()
    user_account = result[1]; end_ddl = result[3]
    current_date = datetime.date.today()
    if current_date <= end_ddl:
        sql_query21 = "UPDATE users SET credit = credit+100 WHERE user_account = %s"
        values21 = (user_account,)
        cursor.execute(sql_query21, values21)

    #更新借阅信息表，删除一条记录
    sql_query3 = "DELETE FROM borrow_info WHERE book_id = %s"
    values3 = (book_id,)
    cursor.execute(sql_query3, values3) 
    db.commit()
    db.close()
    return '已确认还书！'

if __name__ == '__main__':
    app.run(debug=True)