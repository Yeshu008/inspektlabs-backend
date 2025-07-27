from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def welcome():
    return jsonify({"message": "🚗 Welcome to the Vehicle Inspection API"}), 200
