from flask import Flask
from flask_cors import CORS

from routes.user_route import userRoutes
from routes.automata_route import automataRoutes

app = Flask(__name__)
    
if __name__ == "__main__":
    cors = CORS(app)
    app.register_blueprint(userRoutes)
    app.register_blueprint(automataRoutes)
    app.run(debug=True)
