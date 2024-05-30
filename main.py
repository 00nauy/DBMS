import pymysql
from flask import Flask
from flask import request, render_template, redirect, url_for, flash, jsonify, abort
from flask_login import UserMixin, login_user, login_required, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash
import datetime
import threading  
import time
from user_base import User
from manager_base import Manager
from seats import seat_list, timejunc

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



##################################################################
## 用户模块（少数功能用户和管理员可共用）


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
            sql_query = "INSERT INTO users (user_name, password, credit, credit2) VALUES (%s, %s, %s, %s)"
            values = (name, hashed_password, 300, 300) 
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
@app.route('/index', defaults={'page': 1})
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page):
    if not isinstance(current_user, User): 
        abort(403)
    if request.method == "GET":
        # 连接数据库
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()

        # 每页显示6条公告
        items_per_page = 6
        offset = (page - 1) * items_per_page
        cursor.execute("SELECT title, content, pubtime FROM announcements ORDER BY pubtime DESC LIMIT %s OFFSET %s", (items_per_page, offset))  # 查询当前页的公告
        announcements = cursor.fetchall()
        cursor.execute("SELECT COUNT(*) FROM announcements")    # 查询总公告数
        total_count = cursor.fetchone()[0]
        total_pages = (total_count + items_per_page - 1) // items_per_page  # 计算总页数
        db.close()

        return render_template( 'index.html', 
                                username=current_user.name, announcements=announcements, total_pages=total_pages, current_page=page)


#登出页面，当用户或管理员在主页按下“退出登录”按钮时，将退出登录并跳转到登录页面。
@app.route('/logout')  
@login_required  
def logout():  
    logout_user()  
    return redirect(url_for('login')) 


#注销功能，当用户或管理员在主页按下“注销”按钮时，将退出登录并跳转到登录页面，同时账号信息删除。
@app.route('/logoff')  
@login_required  
def logoff():  
    #用户
    if isinstance(current_user, User): 
        user_id = current_user.account
        logout_user()  
        #删除用户信息
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        sql_query = "DELETE FROM users WHERE user_account = %s"
        values = (user_id,)
        cursor.execute(sql_query, values) 
        db.commit()
        db.close() 
    #管理员
    else:
        manager_id = current_user.account
        logout_user()  
        #删除管理员信息
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        sql_query = "DELETE FROM manager WHERE account = %s"
        values = (manager_id,)
        cursor.execute(sql_query, values) 
        db.commit()
        db.close()
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
        username = current_user.name, usercredit = current_user.credit, usercredit2 = current_user.credit2)


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


#座位列表，图书馆一共有100个座位，座位号分别为1到100.
seat_list = [i+1 for i in range(100)]


#预约座位页，当用户在主页按下“预约座位”按钮时，跳转到预约座位页1。
#对应模板文件为'seats.html'，'seats3.html'
@app.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    if not isinstance(current_user, User): 
        abort(403)
    if request.method == "POST":
        hour = request.form.get('hour')
        minute = request.form.get('minute')
        hour2 = request.form.get('hour2')
        minute2 = request.form.get('minute2')

        today = datetime.datetime.today().date()
        start_time = datetime.datetime.combine(today, datetime.time(int(hour), int(minute)))
        end_time = datetime.datetime.combine(today, datetime.time(int(hour2), int(minute2)))
        if(start_time < datetime.datetime.now()):
            return '开始时间不得早于当前时间！'
        if(end_time - start_time < datetime.timedelta(hours=1)):
            return '结束时间须至少比开始时间晚一小时！'
        
        ok_list = [i+1 for i in range(100)]
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        sql_query = "SELECT * FROM seats"
        cursor.execute(sql_query)  
        result = cursor.fetchall()
        for res in result:
            if timejunc(start_time,end_time,res[3],res[4]):
                if int(res[1]) in ok_list:
                    ok_list.remove(int(res[1]))
        db.commit() 
        db.close()
        return render_template('seats3.html',seats=ok_list,t=today,t11=hour,t12=minute,t21=hour2,t22=minute2)
    return render_template('seats.html',seats=seat_list)


#预约座位页2，当用户在预约座位页1按下“查看预约情况”时，将跳转到此页面。
#对应模板文件为'seats2.html'
@app.route('/reserve2', methods=['GET', 'POST'])
@login_required
def reserve2():
    if not isinstance(current_user, User): 
        abort(403)
    if request.method == "GET":
        id = request.args.get('seat_id') 
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        sql_query = "SELECT * FROM seats WHERE place_id = %s AND DATE(start_time) = %s"
        values = (id, datetime.date.today())
        cursor.execute(sql_query, values)  
        result = cursor.fetchall()
        db.commit() 
        db.close()
        if len(result) == 0:
            return '今日无预约记录！'
        return render_template('seats2.html',result=result)


#预约座位页3，当用户在预约座位页1按下”预约“按钮时，将进行相应操作并返回结果。
@app.route('/reserve3', methods=['GET', 'POST'])
@login_required
def reserve3():
    if not isinstance(current_user, User): 
        abort(403)
    #此处检查预约点数是否不足100，若不足100则无法预约
    if current_user.credit2 < 100:
        return '预约点数不足！'
    if request.method == "GET":
        id = request.args.get('seat_id')
        today = datetime.datetime.strptime(request.args.get('t'), '%Y-%m-%d')
        hour = request.args.get('t11')
        minute = request.args.get('t12')
        hour2 = request.args.get('t21')
        minute2 = request.args.get('t22')
        time1 = datetime.datetime.combine(today, datetime.time(int(hour), int(minute)))
        time2 = datetime.datetime.combine(today, datetime.time(int(hour2), int(minute2)))
        print("hahah!",time1, time2)

        #可能存在座位已经被预约的情况，需要排除之
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        sql_query = "SELECT * FROM seats WHERE place_id = %s AND DATE(start_time) = %s"
        values = (id, datetime.date.today())
        cursor.execute(sql_query, values)
        result = cursor.fetchall()
        for res in result:
            if timejunc(time1,time2,res[3],res[4]):
                db.close()
                return '此时间段已有预约！请重新预约！'

        #更新座位信息表，新增一条记录
        sql_query = "INSERT INTO seats (place_id,user_account,start_time,end_time,signed) VALUES (%s, %s, %s, %s, %s)"
        values = (id,current_user.account,time1,time2,0)
        cursor.execute(sql_query, values)  

        #修改用户信息表，扣除100预约点数
        sql_query = "UPDATE users SET credit2 = credit2-100 WHERE user_account = %s"
        values = (current_user.account,)
        cursor.execute(sql_query, values) 
        db.commit() 
        db.close()
        return '预约成功！'


#预约信息页，当用户在主页按下“查询预约信息”按钮时，跳转到预约信息页，展示用户的当前预约。
#对应模板文件为'borrow_info.html'
@app.route('/reserve_info', methods=['GET', 'POST'])
@login_required
def rs_info():
    if not isinstance(current_user, User): 
        abort(403)
    if request.method == "GET":
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        sql_query = "SELECT order_id, place_id, start_time, end_time, signed FROM seats WHERE user_account = %s"
        values = (current_user.account,)  
        cursor.execute(sql_query, values)  
        result = cursor.fetchall()
        info1 = '无预约记录!';info2 = '无预约记录!';info3 = '无预约记录!'
        id_list = []
        if (len(result)>=1):
            if result[0][4] == 1:
                signed = '是'
            else:
                signed = '否'
            id_list.append(result[0][0])
            info1 = '座位号：{} 开始时间：{} 结束时间：{} 签到状态：{}'.format(result[0][1],result[0][2],result[0][3],signed)
        if (len(result)>=2):
            if result[1][4] == 1:
                signed = '是'
            else:
                signed = '否'
            id_list.append(result[1][0])
            info2 = '座位号：{} 开始时间：{} 结束时间：{} 签到状态：{}'.format(result[1][1],result[1][2],result[1][3],signed)
        if (len(result)>=3):
            if result[2][4] == 1:
                signed = '是'
            else:
                signed = '否'
            id_list.append(result[2][0])
            info3 = '座位号：{} 开始时间：{} 结束时间：{} 签到状态：{}'.format(result[2][1],result[2][2],result[2][3],signed)
        db.close()
        return render_template('reserve_info.html', info1=info1,info2=info2,info3=info3,id_list=id_list,length=len(id_list))


#提前结束，当用户在预约信息页按下“提前结束”按钮时，将进行相应操作。
@app.route('/seatend', methods=['GET', 'POST'])
@login_required
def seatend():
    if not isinstance(current_user, User): 
        abort(403)
    #判断预约是否已经结束
    orderid = request.args.get('id')
    db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
    cursor = db.cursor()
    sql_query = "SELECT * FROM seats WHERE order_id = %s"
    values = (orderid,)
    cursor.execute(sql_query, values)
    result = cursor.fetchone()
    if result is None:
        db.close()
        return '预约已经结束了，无需再结束！'

    #修改用户信息表，增加100预约点数
    sql_query = "UPDATE users SET credit2 = credit2+100 WHERE user_account = %s"
    values = (current_user.account,)
    cursor.execute(sql_query, values) 

    #结束预约，更新座位信息表，删除一条记录
    sql_query = "DELETE FROM seats WHERE order_id = %s"
    values = (orderid,)
    cursor.execute(sql_query, values)
    db.commit() 
    db.close()
    return "成功结束预约！"




##################################################################
## 管理员模块



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


#签到页面，当管理员在主页按下“签到管理”按钮时，跳转到此页面，管理员需要在此页面输入用户号，若存在对应记录，则跳转到签到页面2。
#签到页面1对应模板文件为'sign.html'，签到页面2对应模板文件为'sign2.html'
@app.route('/sign', methods=['GET', 'POST'])
@login_required
def seatsign():
    if not isinstance(current_user, Manager): 
        abort(403)
    if request.method == "POST":
        #读取信息
        user_id = request.form['id']  
        if not user_id.isdigit(): 
            return '请输入一个整数！'
        #在座位信息表中根据用户号查询预约记录
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        sql_query = "SELECT * FROM seats WHERE user_account = %s"
        values = (user_id,)
        cursor.execute(sql_query, values) 
        result = cursor.fetchall()
        if len(result) == 0:
            return '无预约记录！'
        db.commit()
        db.close()
        return render_template('sign2.html',result = result) 
    return render_template('sign.html')


#当管理员在签到页面2按下“确认已到”时，进行签到操作并返回操作结果信息。
@app.route('/sign2', methods=['GET', 'POST'])
@login_required
def seatsign2():
    if not isinstance(current_user, Manager): 
        abort(403)
    id = request.args.get('id')
    db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
    cursor = db.cursor()
    #可能存在“确认已到”按钮亮起，但其实已经签到的情况，应该排除之
    sql_query = "SELECT * FROM seats WHERE order_id = %s"
    values = (id,)
    cursor.execute(sql_query, values)
    result = cursor.fetchone()
    if result[5] == 1:
        db.close()
        return '已经签过到了！'
    #如果此时时间比开始时间提前十分钟以上，则无法签到
    if result[3] - datetime.datetime.now() > datetime.timedelta(minutes=10):
        db.close()
        return '在开始时间前十分钟方可签到！'

    #更新座位信息表，将签到信息进行设置
    sql_query1 = "UPDATE seats SET signed = 1 WHERE order_id = %s"
    values1 = (id,)
    cursor.execute(sql_query1, values1) 
    db.commit()
    db.close()
    return '已签到！'


#座位预约自动处理：每分钟系统将自动对数据库进行扫描，对“预约自然结束”和“因未签到导致预约强制结束”两种情况进行相应操作。
def scan_database():  
    print("自动扫描已启动！")
    db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
    cursor = db.cursor()
    while True:  
        # 计算下一分钟的开始时间  
        now = datetime.datetime.now()  
        next_minute = now + datetime.timedelta(minutes=1)  
        next_minute = next_minute.replace(second=0, microsecond=0)  
  
        # 等待到下一分钟的开始  
        wait_time = (next_minute - now).total_seconds()  
        time.sleep(wait_time)  
        print(f"Scanning database at {datetime.datetime.now()}")

        #查找所有开始时间后30min内未签到的座位预约，强制结束预约，用户不会恢复预约点数
        sql_query = "DELETE FROM seats WHERE start_time < %s AND signed = 0"
        values = (datetime.datetime.now()-datetime.timedelta(minutes=30),)
        cursor.execute(sql_query, values) 

        #查找所有满足自然结束条件的座位预约，为用户恢复100预约点数并结束预约
        sql_query = "SELECT user_account FROM seats WHERE end_time < %s"
        values = (datetime.datetime.now(),)
        cursor.execute(sql_query, values) 
        result = cursor.fetchall()
        for i in result:
            #修改用户信息表，增加100预约点数
            sql_query = "UPDATE users SET credit2 = credit2+100 WHERE user_account = %s"
            values = (i[0],)
            cursor.execute(sql_query, values)

        #修改座位信息表，删除相应记录
        sql_query = "DELETE FROM seats WHERE end_time < %s"
        values = (datetime.datetime.now(),)
        cursor.execute(sql_query, values) 
        db.commit()


#座位预约自动处理
def start_database_scanner():  
    thread = threading.Thread(target=scan_database)  
    thread.start()


# 查询页面，用户可以在此页面输入书名、作者、类别进行搜索，搜索结果将显示在同一页面，且用户可以直接借阅。
@app.route('/search', methods=['GET'])
@login_required
def search():
    if request.method == "GET":
        # 从请求中获取参数
        book_name = request.args.get('book', '')
        author = request.args.get('author', '')
        category = request.args.get('class', '')

        # 检查是否有输入搜索条件
        if book_name or author or category:
            db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
            cursor = db.cursor()
            sql_query = """
                        SELECT * FROM books 
                        WHERE book_name LIKE %s AND class LIKE %s AND author LIKE %s
                        """
            values = ('%' + book_name + '%', '%' + category + '%', '%' + author + '%')
            cursor.execute(sql_query, values)
            result = cursor.fetchall()
            db.close()
            # 传递结果到模板，包括一个标识符表示有搜索执行
            return render_template('search.html', result=result, searched=True)
        else:
            # 如果没有任何搜索条件，设置result为空并传递一个标识符表示未执行搜索
            return render_template('search.html', result=None, searched=False)
        
    # 如果不是GET请求，返回空搜索页面
    return render_template('search.html')


# 公告页面，管理员可以在此页面发布公告与删除公告。
@app.route('/announcement', methods=['GET', 'POST'])
@login_required
def announcement():
    #若当前用户不是管理员，则禁止访问
    if not isinstance(current_user, Manager): 
        abort(403)
    if request.method == "POST":
        # 从请求中获取公告内容
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        # 检查标题和内容是否为空
        if not title or not content:
            flash('标题和内容都不能为空！')
            return render_template('announcement.html')
        # 获取当前时间
        current_date = datetime.date.today()
        # 更新数据库
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()
        cursor.execute("SELECT MAX(announcement_id) FROM announcements")
        new_id = cursor.fetchone()[0]
        new_id = new_id + 1 if new_id else 1
        sql_query = "INSERT INTO announcements (announcement_id, title, content, pubtime) VALUES (%s, %s, %s, %s)"
        values = (new_id, title, content, current_date)
        cursor.execute(sql_query, values)
        db.commit()
        db.close()
        return redirect(url_for('announcement'))
    
    # 分页显示公告
    page = request.args.get('page', 1, type=int)
    items_per_page = 20
    offset = (page - 1) * items_per_page

    db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
    cursor = db.cursor()
    cursor.execute("SELECT announcement_id, title, content, pubtime FROM announcements ORDER BY pubtime DESC LIMIT %s OFFSET %s", (items_per_page, offset))
    announcements = cursor.fetchall()

    # 获取总公告数
    cursor.execute("SELECT COUNT(*) FROM announcements")
    total_count = cursor.fetchone()[0]
    db.close()

    total_pages = (total_count + items_per_page - 1) // items_per_page

    return render_template('add_ann.html', announcements=announcements, total_pages=total_pages, current_page=page)


@app.route('/delete_announcement/<int:id>', methods=['POST'])
@login_required
def delete_announcement(id):
    if not isinstance(current_user, Manager): 
        abort(403)  # 只有验证过的用户可以删除公告
    db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
    cursor = db.cursor()
    cursor.execute("DELETE FROM announcements WHERE announcement_id = %s", (id,))
    db.commit()
    db.close()
    flash('公告已删除')
    return redirect(url_for('announcement'))  # 删除后重定向到公告页面



if __name__ == '__main__':
    start_database_scanner()
    app.run(debug=True)