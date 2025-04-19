# D:\Ahh\Projects\story\backend\app.py

from flask import Flask
from flask_cors import CORS
from routes import routes

app = Flask(__name__)

# Apply CORS globally
CORS(app, resources={r"/*": {"origins": "*"}})

# Apply CORS to the blueprint (optional but safe)
CORS(routes)

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
