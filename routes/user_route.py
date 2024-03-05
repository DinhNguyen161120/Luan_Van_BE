
import datetime
from flask import Blueprint, jsonify, request
from dbs.configMongoDB import get_database
from bson.json_util import dumps

userRoutes = Blueprint("userRoutes", __name__)

@userRoutes.route('/auth/login', methods = ['POST'])
def login():
    mydb = get_database()
    userCol = mydb["Users"]
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = userCol.find_one({'email': email})
    if  user is None:
        return "Email không tồn tại", 500
    
    if user["password"] != password:
        return "Mật khẩu không chính xác", 500
    
    #     delete user.password
    user['password'] = ''
    user['_id'] = str(user['_id'])
    return jsonify({
        "message": 'Login success',
        "code": 'login0',
        "metadata": {
            "userDetails": dumps(user)
        }
    })

@userRoutes.route('/auth/register', methods = ['POST'])
def register():
    data = request.json
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get('password')

    mydb = get_database()
    userCol = mydb["Users"]
    user = userCol.find_one({'email': email})
    if  user:
        return "Email đã tồn tại", 500
    

    x = userCol.insert_one({
        "email": email,
        "password": password,
        "firstName": firstName, 
        "lastName": lastName
    })

    folderCol = mydb["folders"]
    folderCol.insert_one({
        "name": 'My Drive',
        "user": x.inserted_id,
        "parent": x.inserted_id,
        "dateCreate": datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
        "size": '',
        "type": 'folder',
        "path": '/My Drive'
    })
    user = userCol.find_one({'email': email})
    return jsonify({
        "message": 'Register success',
        "code": 'register0',
        "metadata": {
            "userDetails": dumps(user)
        }
    })



