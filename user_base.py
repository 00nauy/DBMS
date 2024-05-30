import pymysql
from flask_login import UserMixin
from werkzeug.security import check_password_hash
  
class User(UserMixin):  
    def __init__(self, account, name, hash_password, credit, credit2):  
        self.account = account
        self.name = name
        self.hash_password = hash_password
        self.credit = credit
        self.credit2 = credit2
    
    def get_id(self):
        return self.account
  
    @staticmethod  
    def get_by_account(account):   
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")  
        cursor = db.cursor()   
        sql_query = "SELECT user_name, password, credit, credit2 FROM users WHERE user_account = %s" 
        values = (account,)  
        cursor.execute(sql_query, values)  
        result = cursor.fetchone()  
        db.close()  
        if result:  
            return User(account, result[0], result[1], result[2], result[3])  
        return None  
  
    def check_password(self, password):  
        return check_password_hash(self.hash_password, password)

