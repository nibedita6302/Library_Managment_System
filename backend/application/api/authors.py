import os
from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from security import datastore
from flask import request, jsonify, current_app as app
from flask_login import current_user
from flask_security import auth_required, roles_required

from application.models.books import Author, AuthorBook

author_field = {
    'a_id': fields.Integer,
    'a_name': fields.String,
    'about_author': fields.String
}

class AuthorManagement(Resource):
    def get(self, author_id):       ## Get Author details 
        author = Author.query.get(author_id)
        if not author:
            return {'message': {'error': 'Author Not Found'}}, 404
        return marshal(author, author_field), 200

    @auth_required('token')
    @roles_required('librarian')
    def post(self):                 ## Create new Author 
        jsonData = request.get_json()
        if ('a_name' in jsonData) and ('about_author' in jsonData):
            if not Author.query.filter_by(a_name=jsonData['a_name']).first():
                author = Author(**jsonData)
                db.session.add(author)
                db.session.commit()
                return {'message': {'success': 'New Author Created!'}}, 200
            return {'message':{'error': 'Author Name must be Unique'}}, 400
        return {'message': {'error': 'All fields are compulsory.'}}, 400

    @auth_required('token')
    @roles_required('librarian')
    def put(self, author_id):                  ## Update Author details
        jsonData = request.get_json() 
        author = Author.query.get(author_id)
        if ('a_name' in jsonData) and (jsonData['a_name']!=''):
            author.a_name = jsonData['a_name']
        elif ('about_author' in jsonData) and (jsonData['about_author']!=''):
            author.about_author = jsonData['about_author']
        else:
            return {'message': {'error': 'Atleast one field needs to be filled!'}}, 400
        
        db.session.commit()
        return {'message': {'success': 'Author Updated!'}}, 200

    @auth_required('token')
    @roles_required('librarian')
    def delete(self, author_id):  
            author = Author.query.get(author_id)
            print(author.biblography)
            if author.biblography != []:          ## Check if any book id writen by author
                return {'message': 
                        {'error': 'Cannot delete Author because it still has associated books. Please delete all books written by this Author.'}
                    }, 409   
            db.session.delete(author)
            db.session.commit()
            return {'message': {'success': f'Author with ID {author.a_id} deletion confirmed!'}}, 200
    
class AuthorDisplay(Resource):
    @roles_required('librarian')
    def get(self):                      ## Get All Authors 
        author = Author.query.all()
        return marshal(author, author_field), 200