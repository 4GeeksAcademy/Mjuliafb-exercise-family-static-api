"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_member():
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def handle_member_id(member_id):
    members = jackson_family.get_member(member_id)
    if members:
        return jsonify(members), 200
    else:
        return jsonify({"msg":"member doesn't exist"}), 400
    
@app.route('/members', methods=['POST'])
def handle_add_member():
    member = request.get_json()
    if not member:
        return jsonify({"msg": "No member data provided"}), 400
    required_fields = ["id","first_name", "last_name", "age", "lucky_numbers"]
    if not all(field in member for field in required_fields):
        return jsonify({"msg": "Missing required fields"}), 400
    if len(member.keys()) != len(required_fields):
        return jsonify({"msg": "Extra fields provided"}), 400
    members = jackson_family.add_member(member)
    if members:
        return jsonify({"msg": "Member added successfully"}), 200
    else:
        return jsonify({"msg": "Unable to add member"}), 400

@app.route('/members/<int:member_id>', methods=['DELETE'])
def handle_delete_id(member_id):
    members = jackson_family.delete_member(member_id)
    if members:
        return jsonify({"msg" : "member deleted successfully"}), 200
    else:
        return jsonify({"msg":"couldn't delete member"}), 400



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
