import os
from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from security import datastore
from flask import request, jsonify, current_app as app
from flask_login import current_user
from flask_security import auth_required, roles_required

from application.models.books import Author, AuthorBook

class AuthorManagement(Resource):
    def get(self, author_id):       ## Get Author details 
        author = Author.query.get(author_id)

    def post(self):                 ## Create new Author 
        pass 

    def put(self):                  ## Update Author details
        pass 

    def delete(self):               ## Delete Author details
        ## Deletion of Author deletes books??
        pass