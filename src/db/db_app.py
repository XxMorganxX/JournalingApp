from flask import Flask, Blueprint, request, jsonify
from db import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
db_api = Blueprint('db_api', __name__)

app = Flask(__name__)


@db_api.route('/register', methods=['POST'])
def register():
    """
    Create a new user account
    """
    body = request.get_json()
    
    # Check if required fields are present
    if not all(k in body for k in ["email", "password", "name"]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=body["email"]).first():
        return jsonify({"error": "Email already registered"}), 409
    
    # Create new user with hashed password
    hashed_password = generate_password_hash(body["password"])
    new_user = User(
        email=body["email"],
        password=hashed_password,
        name=body["name"]
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.serialize()), 201

@db_api.route('/login', methods=['POST'])
def login():
    """
    Sign in existing user
    """
    body = request.get_json()
    
    # Check if required fields are present
    if not all(k in body for k in ["email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Find user by email
    user = User.query.filter_by(email=body["email"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Verify password
    if not check_password_hash(user.password, body["password"]):
        return jsonify({"error": "Invalid password"}), 401
    
    return jsonify(user.serialize()), 200

@db_api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_account(user_id):
    """
    Delete user account and all associated journal entries
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "Account deleted successfully"}), 200


if __name__ == "__main__":
    
    
    import os
    
    load_dotenv("constants.env")
    
    # Get host and port from environment variables or use defaults
    DB_HOST = os.getenv("INTERNAL_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("INTERNAL_PORT", 8000))
    
    
    app.run(host=DB_HOST, port=DB_PORT, debug=True)