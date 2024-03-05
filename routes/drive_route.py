
import datetime
from flask import Blueprint, jsonify, request
from dbs.configMongoDB import get_database
from bson.json_util import dumps
from bson import ObjectId

driveRoutes = Blueprint("driveRoutes", __name__)

@driveRoutes.route('/drive/create-folder', methods = ['POST'])
def createFolder():
    mydb = get_database()
    data = request.json
    name = data.get('name')
    parentId = data.get("parentId")
    userId = data.get("userId")
    path = data.get("path")
    folderCol = mydb["folders"]
    folderCol.insert_one({
        "name": name,
        "user": ObjectId(userId),
        "parent": ObjectId(parentId),
        "dateCreate": datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
        "size": '',
        "type": 'folder',
        "path": path
    })
    return "Tạo thư mục thành công", 200

@driveRoutes.route('/drive/get-all-folder', methods = ['POST'])
def getAllFolder():
    mydb = get_database()
    data = request.json
    userId = data.get("userId")
    print(userId, "======")
    folderCol = mydb["folders"]
    folders = folderCol.aggregate([
        {
            "$match": {"user": ObjectId(userId)}
        },
        {
            '$lookup': {
                'from': 'folders', 
                'localField': 'parent',
                'foreignField': '_id',
                'as': 'parent'
            }
        }
    ])
    listFolders = list(folders)
    resData = list()
    for folder in listFolders:
        folder["_id"] = str(folder["_id"])
        folder["user"] = str(folder["user"])
        if len(folder['parent']) != 0:
            folder['parent'] = dict(folder["parent"][0])
            folder['parent']['_id'] = str(folder['parent']['_id'])
            folder['parent']['user'] = str(folder['parent']['user'])
            folder['parent']['parent'] = str(folder['parent']['parent'])
        resData.append(folder)
    return jsonify(resData)