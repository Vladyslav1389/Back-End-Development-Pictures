from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

# data = []
######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
    else:
        return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    try:
        if not data:
            return {"message": "data is not exist"}, 500
        for url in data:
            if url["id"] == id:
                return url, 200
        return {"message": "Url is not found"}, 404
    except Exception as e:
        return {"message": f"Something went wrong: {e}"}, 500



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        if not data:
            return {"message": "data is not exist"}, 500

        new_picture = request.get_json()
        if not new_picture:
            return {"message": "A query parameter is missing"}, 400

        for picture in data:
            if new_picture["id"] == picture["id"]:
                return {
                    "Message": f"picture with id {new_picture['id']} already present"
                }, 302

        data.append(new_picture)
        # return {"message": "New picture was appended succesfully!"}, 201
        return new_picture, 201

    except Exception as e:
        return {"message": f"Something went wrong: {e}"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    try:
        if not data:
            return {"message": "data is not exist"}, 500
        
        new_picture = request.get_json()
        if not new_picture:
            return {"message": "Your body is empty"}, 400

        for i, picture in enumerate(data):
            if id == picture["id"]:
                data[i] = new_picture
                return new_picture, 302

        return {"message": f"Picture with id {id} not found"}, 404

    except Exception as e:
        return {"message": f"Something went wrong: {e}"}, 400

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pass
