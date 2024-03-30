import os
from datetime import datetime, timedelta
from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from flask import request, jsonify, current_app as app
from flask_login import current_user
from flask_security import auth_required, roles_required

from application.models.books import Sections, Books
from application.models.user_book_activity import UserActivity, IssueRequest, UserBook
from application.models.users import Users
from application.jobs.Tasks.bookIssueStatusEmail import *


section_read_field = {
    'section_name': fields.String,
    'count': fields.Integer
}

section_revenue_field = {
    'section_name': fields.String,
    'revenue': fields.Float
}

active_users_field = {
    'name': fields.String
}

class LibrarianAnalytics(Resource):
    @auth_required('token')
    @roles_required('librarian')
    def get(self):      
        ## Section wise user-read distribution 
        section_read_count = db.session.query(Sections.s_name.label('section_name'), 
                                            db.func.sum(Books.total_issue).label('count'))\
                                .filter(Books.s_id==Sections.s_id)\
                                .group_by(Sections.s_id).all()
        
        ## Section wise revenue distribution
        section_revenue =  db.session.query(UserActivity.section_name, 
                                            db.func.sum(UserActivity.bought_price).label('revenue'))\
                            .filter(Sections.s_name==UserActivity.section_name)\
                            .group_by(UserActivity.section_name).all()

        ## Most Active Users
        active_users = db.session.query(Users.name)\
                        .join(UserActivity, Users.id==UserActivity.user_id)\
                        .group_by(Users.id).order_by(db.func.count('*').desc()).all()

        return {
            'section_read_distribution': marshal(section_read_count, section_read_field),
            'section_revenue': marshal(section_revenue, section_revenue_field),
            'active_users': marshal(active_users, active_users_field)
        }, 200
        
class Issue_Request_Approval(Resource):
    @auth_required('token')
    @roles_required('librarian')
    def put(self, book_id, user_id):                    ## Accept / Reject request
        jsonData = request.get_json()
        ir1 = IssueRequest.query.filter_by(b_id=book_id, user_id=user_id).first()
        book = Books.query.get(book_id)

        if ('approval' in jsonData) and (ir1 is not None):
            if ir1.status!=2:
                return {'message':{'error':'The issue had been already Accepted or Rejected'}}, 400
            if jsonData['approval']==1:             ## Accept Request
                ir1.status = jsonData['approval']

                ## create UserBook association
                user_book = UserBook(b_id=book_id, user_id=user_id) 
                db.session.add(user_book)

                if book.total_issue is not None:
                    book.total_issue+=1                 ## Increment Total Issues in Book
                else:
                    book.total_issues=1

                ## Create User Activity Instance
                section = Sections.query.get(book.s_id)
                author = book.writer[0]                
                user_actv = UserActivity(user_id=user_id, book_name=book.b_name, 
                                         section_name = section.s_name, author_name=author.a_name,
                                         issue_date = user_book.issue_date)     
                db.session.add(user_actv)
                db.session.commit()

                ## Send mail to User - Celery
                issue_approval_email.delay(user_id, book.b_name, "APPROVED")
                return {'message':{'success':'Issue Request has been Accepted'}}, 200
            
            elif jsonData['approval']==0:
                ir1.status = jsonData['approval']
                db.session.commit()
                
                ## Send mail to User - Celery
                issue_approval_email.delay(user_id, book.b_name, "DECLINED")
                return {'message':{'success':'Issue Request has been Rejected'}}, 200
            
            else:
                return {'message':{'error':'Invalid approval code'}}, 400
        return {'message':{'error':'Bad Request or Issue does not exists'}}, 400
    
    @auth_required('token')
    @roles_required('librarian')
    def post(self, issue_id):                       ## Revoke Request
        user_book = UserBook.query.get(issue_id)
        if (user_book is not None) and (user_book.revoked!=1):
            ## 1 day warning before Revoke
            revoke_due = datetime.now() + timedelta(days=1)     
            ## Due date set to revoke_due or due_date, which ever is Earliest
            user_book.due_date = min(user_book.due_date, revoke_due)   
            user_book.revoked = 1
            db.session.commit()

            ## Send email to user
            revoke_issue_email.delay(user_book.user_id, user_book.b_id)

            return {'message':{'success':'Revoke successfull with 1 day warning'}}, 200
        return {'message':{'error':'Book already Revoked'}}, 400

        
