
from flask import Blueprint, jsonify

userRoutes = Blueprint("userRoutes", __name__)
@userRoutes.route('/')
def index():
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com'})



