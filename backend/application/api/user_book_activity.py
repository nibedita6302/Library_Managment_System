import os
from datetime import datetime
from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from security import datastore
from flask import request, jsonify, current_app as app
from flask_login import current_user
from flask_security import auth_required, roles_required

from application.models.user_book_activity import UserBook, UserActivity, IssueRequest
from application.models.books import Books
from application.models.users import Users

issue_req_field = {
    'user_id': fields.Integer,
    'b_id': fields.Integer,
    'status': fields.Integer,
}

class Issue_Book_Request(Resource):
    @auth_required('token')
    def get(self):                  ## Get all book issues
        if 'librarian' in current_user.roles:
            ir1 = IssueRequest.query.all()      ## Return all requests to Librarian
        else:
            ir1 = IssueRequest.query.filter_by(user_id=current_user.id).all()   ## Return only user's requests
        return marshal(ir1, issue_req_field), 200

    @auth_required('token')
    @roles_required('user')
    def post(self, book_id):        ## Request for book issue 
        if len(current_user.user_book)==5:      ## Maximum issue limit = 5 books
            return {'message':{'error':'Issue Request Declines. You can issue upto 5 book at a time'}}, 400
        user_books = UserBook.query.filter_by(user_id=current_user.id,      ## Book issued by user 
                                              b_id=book_id,                 ## But not returned yet
                                              return_date=None).first()
        if user_books is not None:
            return {'message':{'error':'You have already issued this book. Visit MyBooks to read.'}}, 400
        
        ir = IssueRequest.query.filter_by(user_id=current_user.id, b_id=book_id).first()
        if ir:
            if ir.status==2:        ## Issue request pending
                return {'message':{
                    'success':'Please wait while your issue is under process',
                    'status': 'PENDING' 
                }}, 400
            if ir.status==0:        ## Issue request rejected
                return {'message':{
                    'success':'Your issue has been declined, please try again after few days.',
                    'status': 'REJECTED' 
                }}, 400
            
        ir1 = IssueRequest(user_id=current_user.id, b_id = book_id)
        db.session.add(ir1)
        db.session.commit()
        return {'message':{'success':'Issue Request sent to Librarian. Please wait for confirmation'}}, 200

    @auth_required('token')
    @roles_required('user')
    def put(self, issue_id):         ## Return book 
        user_book = UserBook.query.get(issue_id)
        book = Books.query.get(user_book.b_id)
        user_actv = UserActivity.query.filter_by(user_id=current_user.id, book_name=book.b_name,
                                                  return_date=None).first()
        if (user_book is None) or (user_book.user_id!=current_user.id):     ## Issue does not exists for current user
            return {'message':{'error':'This book is not issued by you, yet.'}}, 400
        if user_book.return_date is not None:                         ## Already returned book
            return {'message':{'error':'The book has already been returned!'}}, 400
        ## Set return date in UserBooks and UserActivity
        user_book.return_date = datetime.now()
        user_actv.return_date = datetime.now()
        db.session.commit()
        return {'message':{'success':'Book returned successfully'}}, 200

section_count_field = {
    'section_name': fields.String,
    'count': fields.Integer
}

fav_author_field = {
    'author_name': fields.String,
    'count': fields.Integer
}

ranking_field = {
    'name': fields.String,
    'count': fields.Integer
}

class UserStats(Resource):
    @auth_required('token')
    @roles_required('user')
    def get(self):
        ## Section Wise Distribution
        section_count = db.session.query(UserActivity.section_name, db.func.count().label('count'))\
                        .filter(UserActivity.user_id==current_user.id)\
                        .group_by(UserActivity.section_name).all()
        
        ## Favourite Author
        fav_author = db.session.query(UserActivity.author_name, db.func.count().label('count'))\
                        .filter(UserActivity.user_id==current_user.id)\
                        .group_by(UserActivity.author_name).all()
        
        ## Ranking in different book reads (top 3 & current user rank)
        ranking = db.session.query(Users.name, db.func.count().label('count'))\
                    .join(UserActivity, Users.id==UserActivity.user_id)\
                    .group_by(UserActivity.user_id).all()
        
        return {
            'section_distribution': marshal(section_count, section_count_field),
            'favourite_author': marshal(fav_author, fav_author_field),
            'ranking': marshal(ranking, ranking_field)
        }, 200