from pymongo import MongoClient
def get_database():
    myClient = MongoClient("mongodb://localhost:27017/")
    mydb = myClient["automata"]
    return mydb
