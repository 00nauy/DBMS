import pymysql
from flask import Flask
from flask import request, render_template, redirect, url_for, flash
from flask_login import UserMixin, login_user, login_required, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

if __name__ == '__main__':
    # #上架书籍
    # db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
    # cursor = db.cursor()
    # sql_query = "INSERT INTO books (book_name,class,author,publisher,pubtime,entertime,borrowed) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # values = ("机器学习001","计算机","作者001","出版社001","2017-05-01","2023-05-01",0) 
    # cursor.execute(sql_query, values)  
    # db.commit()
    # db.close()

    # db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
    # cursor = db.cursor()
    # sql_query = "UPDATE books SET borrowed = 0 WHERE book_id = %s"
    # values = (4,)
    # cursor.execute(sql_query, values) 
    # db.commit() 
    # db.close()

    date_time_str1 = "2024-05-29 9:30"
    date_time_obj1 = datetime.datetime.strptime(date_time_str1, "%Y-%m-%d %H:%M")
    date_time_str2 = "2024-05-29 19:30"
    date_time_obj2 = datetime.datetime.strptime(date_time_str2, "%Y-%m-%d %H:%M")
    db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
    cursor = db.cursor()
    sql_query = "INSERT INTO seats (place_id,user_account,start_time,end_time,signed) VALUES (%s, %s, %s, %s, %s)"
    values = (4,132,date_time_obj1,date_time_obj2,0) 
    cursor.execute(sql_query, values)  
    db.commit()
    db.close()
    print("完成！")