from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from security import datastore
from flask import request, jsonify, current_app as app
from flask_login import current_user
from flask_security import auth_required, roles_required

from application.models.books import Books, Sections, Author 

book_field = {
    "b_id": fields.Integer,
    "s_id": fields.Integer,
    "a_id": fields.Integer,
    "b_name": fields.String,
    "b_image": fields.String,
    "pdf_price": fields.Float,
    "date_published": fields.DateTime,
    "publisher": fields.String,
    # "summary": fields.String,
    # "content_link_view": fields.String,
    "total_issue": fields.Integer,
    "total_bought": fields. Integer
}


class SearchBooks(Resource):
    def post(self):
        jsonData = request.get_json() 
        print(jsonData)
        if ('search' not in jsonData) and (jsonData['search'].strip() == ''):
            return {"message":
                    {"error":"No matching book found. Please check for any spelling mistakes!"}
                }, 404
        string = jsonData['search'].lower().strip()
        book_list = []
        for s in string.split():
            item = '%'+s+'%'
            b1 = Books.query.filter(Books.b_name.ilike(item)).all()             ## Search by Book Name
            book_list.extend(b1)
            b2 = Books.query.filter(Books.publisher.ilike(item)).all()          ## Search by Publisher
            book_list.extend(b2) 
            authors = Author.query.filter(Author.a_name.ilike(item)).all()      ## Search by Author 
            for a in authors:
                print(a.biblography)
                book_list.extend(a.biblography) 
            sections = Sections.query.filter(Sections.s_name.ilike(item)).all() ## Search by Section
            for s in sections:
                b3 = Books.query.filter_by(s_id=s.s_id).all()
                book_list.extend(b3) 
        if book_list==[]:
            return {"message":
                    {"error":"No matching book found. Please check for any spelling mistakes!"}
                }, 404
        return marshal(list(set(book_list)), book_field), 200                   ## Return only distinct books
        