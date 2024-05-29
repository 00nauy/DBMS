import pymysql
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class Manager(UserMixin):  
    def __init__(self, account, name, hash_password):  
        self.account = account
        self.name = name
        self.hash_password = hash_password
    
    def get_id(self):
        return self.account
  
    @staticmethod  
    def get_by_account(account):  
        db = pymysql.connect(host="mysql.sqlpub.com", port=3306, user="nauy00", password="YXEh8qSbjeAFwVYO", database="library_system24")
        cursor = db.cursor()  
        sql_query = "SELECT name, password FROM manager WHERE account = %s"  
        values = (account,)  
        cursor.execute(sql_query, values)  
        result = cursor.fetchone()  
        db.close()  
        if result:  
            return Manager(account, result[0], result[1])  
        return None  
  
    def check_password(self, password):  
        return check_password_hash(self.hash_password, password)