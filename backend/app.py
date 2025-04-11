# D:\Ahh\Projects\story\backend\app.py

from flask import Flask
from flask_cors import CORS
from routes import routes

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend-backend communication

# Register the blueprint for routes
app.register_blueprint(routes)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
