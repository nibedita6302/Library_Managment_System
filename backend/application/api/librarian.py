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
from utils.generateGraphs import lib_bar_chart, lib_pie_chart
from application.jobs.Tasks.bookIssueStatusEmail import *

active_users_field = {
    'name': fields.String,
    'book_issue': fields.Integer
}

class LibrarianAnalytics(Resource): 
    @auth_required('token')
    @roles_required('librarian')
    def get(self):      
        ## Section wise user-read distribution 
        book_read_count = db.session.query(Books.b_name.label('book_name'), 
                                           Books.total_issue.label('count')).all()
        print(book_read_count)
        book_read_path = lib_bar_chart(book_read_count, 'Book Popularity in Users', 'lib_book_read_bar')
        
        ## Section wise revenue distribution
        section_revenue =  db.session.query(UserActivity.section_name, 
                                            db.func.sum(UserActivity.bought_price).label('revenue'))\
                            .filter(Sections.s_name==UserActivity.section_name)\
                            .group_by(UserActivity.section_name).all()
        section_revenue_path = lib_pie_chart(section_revenue, 'Section Wise Revenue', 'lib_section_revenue_pie')
        
        ## Most Active Users
        active_users = db.session.query(Users.name, db.func.count('*').label('book_issues'))\
                        .join(UserActivity, Users.id==UserActivity.user_id)\
                        .group_by(Users.id).order_by(db.func.count('*').desc()).all()

        return {
            'book_read_path': book_read_path,
            'section_revenue_path': section_revenue_path,
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

                issue_instance = UserBook.query.filter_by(b_id=book_id, user_id=user_id, return_date=None).first()
                if issue_instance is not None:      ## Check if book already exists
                    ir1.status = 0
                    db.session.commit()
                    ## Send mail to User - Celery
                    issue_approval_email.delay(user_id, book.b_name, "DECLINED")
                    return {'message':{'success':'Issue Declined! Book Already Issued by user.'}}, 200
                
                active_issue_count = UserBook.query.filter_by(user_id=user_id, return_date=None).all()
                if len(active_issue_count)==5:      ## Check if book limit reached
                    ir1.status = 0
                    db.session.commit()
                    ## Send mail to User - Celery
                    issue_approval_email.delay(user_id, book.b_name, "DECLINED")
                    return {'message':{'success':'Issue Declined! User has reached max limit 5 for issues.'}}, 200
                
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
