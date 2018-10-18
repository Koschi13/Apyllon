"""Provide the routes for users interaction"""
from flask import (
    request,
    jsonify)
from flask.views import MethodView

from backend.api.routes import exceptions
from backend.database import user_utils
from backend.database.exceptions import Exists


class UsersIdView(MethodView):
    def get(self, uid: int):
        try:
            user = user_utils.get_user(uid=uid)
        except KeyError as e:
            print(e)
            raise

        if not user:
            return f"User <{uid}> not found", 404

        return jsonify(user.to_dict())

    def put(self, uid: int):
        if not request.is_json:
            raise exceptions.BadRequest("Missing user json", {
                'username': 'Biskit1943',
                'password': 'blake2 hash',
            })
        return f"PUT /users/{uid} + json"

    def delete(self, uid: int):
        try:
            user_utils.delete_user(uid=uid)
        except KeyError:
            raise
        except NameError:
            return f"User <{uid}> not found", 404

        return f"Deleted user <{uid}>", 200


class UsersNameView(MethodView):
    def get(self, username: str):
        try:
            user = user_utils.get_user(username=username)
        except KeyError as e:
            print(e)
            raise

        if not user:
            return f"User <{username}> not found", 404

        return jsonify(user.to_dict())

    def put(self, username: str):
        if not request.is_json:
            raise exceptions.BadRequest("Missing user json", {
                'username': 'Biskit1943',
                'password': 'blake2 hash',
            })
        return f"PUT /users/{username} + json"

    def delete(self, username: str):
        try:
            user_utils.delete_user(username=username)
        except KeyError:
            raise
        except NameError:
            return f"User <{username}> not found", 404

        return f"Deleted user <{username}>", 200


class UserView(MethodView):
    def get(self):
        return jsonify(user_utils.list_users())

    def post(self):
        if not request.is_json:
            raise exceptions.BadRequest("Missing user json", {
                'username': 'Biskit1943',
                'password': 'blake2 hash',
            })

        try:
            user = user_utils.add_user(request.data)
        except Exists as e:
            raise exceptions.Conflict(str(e))
        return jsonify(user.to_dict())