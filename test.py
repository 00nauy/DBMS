import mysql.connector  
from mysql.connector import Error  
from passlib.hash import sha256_crypt

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
  
def register_user(username, password):  
    try:  
        connection = mysql.connector.connect(  
            host='localhost',  
            database='library_system',  
            user='root',  
            password='egwegwegw612'  
        )  
        if connection.is_connected():  
            cursor = connection.cursor()  
            # hashed_password = sha256_crypt.encrypt(password)
            sql_query = "INSERT INTO users (user_name, password, credit) VALUES (%s, %s, %s)"  
            values = (username, password, 300)  
            cursor.execute(sql_query, values)  
            connection.commit()  
            print(f"User '{username}' registered successfully!")  
        else:  
            print("Failed to connect to MySQL database")  
    except Error as e:  
        print(f"Error while connecting to MySQL: {e}")  
    finally:  
        if (connection.is_connected()):  
            cursor.close()  
            connection.close()  


def login_user(account, password):  
    try:  
        connection = mysql.connector.connect(  
            host='localhost',  
            database='library_system',  
            user='root',  
            password='egwegwegw612'  
        )  
        if connection.is_connected():  
            cursor = connection.cursor()  
            sql_query = "SELECT password FROM users WHERE user_account = %s"  
            values = (account,)  
            cursor.execute(sql_query, values)  
            result = cursor.fetchone()  
            if result is not None:  
                stored_password = result[0]  
                # if sha256_crypt.verify(password, stored_password):  
                #     print(f"User '{username}' logged in successfully!")  
                #     # 在这里可以添加更多逻辑，如设置会话、生成令牌等  
                if password == stored_password:
                    print(f"User '{account}' logged in successfully!")  
                else:  
                    print("Invalid password!")  
            else:  
                print("User not found!")  
        else:  
            print("Failed to connect to MySQL database")  
    except Error as e:  
        print(f"Error while connecting to MySQL: {e}")  
    finally:  
        if (connection.is_connected()):  
            cursor.close()  
            connection.close()  

  
# register_user('john_doe', 'mypassword')
# login_user(125, 'mypassword')