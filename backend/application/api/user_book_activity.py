import os
from datetime import datetime
from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from security import datastore
from flask import request, jsonify, current_app as app
from flask_login import current_user
from flask_security import auth_required, roles_required

from application.models.user_book_activity import UserBook, UserActivity, IssueRequest
from application.models.books import Books, Sections, Author
from utils.generateGraphs import create_bar_graph, create_pie_chart
from utils.analytics import *

current_issue_fields = {
    'issue_id': fields.Integer,
    'b_id': fields.Integer,
    'b_name': fields.String,
    'pdf_price': fields.Float,
    's_name': fields.String,
    'a_name': fields.String,
    'issue_date': fields.DateTime,
    'due_date': fields.DateTime,
}

class Issue_Book_Request(Resource):
    @auth_required('token')
    def get(self):                      ## Get current book issues
        if 'librarian' in current_user.roles:
            ## All current issues
            issues = db.session.query(UserBook.issue_id, UserBook.b_id, UserBook.issue_date, UserBook.due_date,
                                  Books.b_name, Books.pdf_price, Sections.s_name, Author.a_name)\
                            .join(Books, UserBook.b_id==Books.b_id)\
                            .join(Sections, Books.s_id==Sections.s_id)\
                            .join(Author, Books.a_id==Author.a_id)\
                            .filter(UserBook.return_date==None).all()
        else:
            ## Current issue for User-ID
            issues = db.session.query(UserBook.issue_id, UserBook.b_id, UserBook.issue_date, UserBook.due_date,
                                  Books.b_name, Books.pdf_price, Sections.s_name, Author.a_name)\
                            .join(Books, UserBook.b_id==Books.b_id)\
                            .join(Sections, Books.s_id==Sections.s_id)\
                            .join(Author, Books.a_id==Author.a_id)\
                            .filter(UserBook.user_id==current_user.id, UserBook.return_date==None).all()
            
        return marshal(issues, current_issue_fields), 200

    @auth_required('token')
    @roles_required('user')
    def post(self, book_id):        ## Request for book issue 
        if len(current_user.user_book)==5:      ## Maximum issue limit = 5 books
            return {'message':{'error':'Issue Request Declines. You can issue upto 5 book at a time'}}, 400
        book = Books.query.get(book_id)
        if not book:
            return {'message':{'error':'Issue Request Declines. Book does not exist'}}, 400

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
                }}, 200
            if ir.status==0:        ## Issue request rejected
                return {'message':{
                    'success':'Your issue has been declined, please try again after few days.',
                    'status': 'REJECTED' 
                }}, 200
            
        ir1 = IssueRequest(user_id=current_user.id, b_id = book_id)
        db.session.add(ir1)
        db.session.commit()
        return {'message':{'success':'Issue Request sent to Librarian. Please wait for confirmation'}}, 200

    @auth_required('token')
    @roles_required('user')
    def put(self, issue_id):                        ## Return book 
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

issue_req_field = {
    'user_id': fields.Integer,
    'b_id': fields.Integer,
    'b_name': fields.String,
    's_name': fields.String,
    'a_name': fields.String,
}

class PendingIssues(Resource):
    @auth_required('token')
    def get(self):                                               ## Get pending book issues
        if 'librarian' in current_user.roles:
            ## Return all pending requests 
            pending_req = db.session.query(IssueRequest.user_id, IssueRequest.b_id, 
                                   Books.b_name, Sections.s_name, Author.a_name)\
                            .join(Books, IssueRequest.b_id==Books.b_id)\
                            .join(Sections, Books.s_id==Sections.s_id)\
                            .join(Author, Books.a_id==Author.a_id)\
                            .filter(IssueRequest.status==2).all()  
        else:
            ## Return only user's pending requests
            pending_req = db.session.query(IssueRequest.user_id, IssueRequest.b_id,
                                   Books.b_name, Sections.s_name, Author.a_name)\
                            .join(Books, IssueRequest.b_id==Books.b_id)\
                            .join(Sections, Books.s_id==Sections.s_id)\
                            .join(Author, Books.a_id==Author.a_id)\
                            .filter(IssueRequest.user_id==current_user.id, IssueRequest.status==2).all() 
            
        return marshal(pending_req, issue_req_field), 200


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
    'issue_count': fields.Integer
}

class UserStats(Resource):
    @auth_required('token')
    @roles_required('user')
    def get(self):
        month = datetime.now().strftime('%B')
        year = datetime.now().strftime('%Y')

        ## Section Wise Distribution - Book Reads
        section_count = section_distribution_user(current_user.id)
        data1 = {}
        for obj in section_count:                                                   ## Convert to dictionary
            data1[obj.section_name] = obj.count
        image_path1 = create_pie_chart(data=data1, title='Reader Preference Pie',    ## Add the pie chart
                    filename=f'pie_{month}_{year}',save_to=1) 
        
        ## Favourite Author
        author = fav_author(current_user.id)
        data1 = {}
        for obj in author:                                                    ## Convert to dictionary
            data1[obj.author_name] = obj.count
        image_path2 = create_bar_graph(data=data1, title='Author Read-o-Meter',    ## Add the pie chart
                                    filename=f'bar_{month}_{year}',save_to=1) 
         
        ## Ranking in different book reads (top 3 & current user rank)
        ranking = user_ranking()
        
        return {
            'section_dist_path': image_path1,
            'fav_author_path': image_path2,
            'ranking': marshal(ranking, ranking_field)
        }, 200
