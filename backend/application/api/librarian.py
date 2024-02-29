import os
from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from security import datastore
from flask import request, jsonify, current_app as app
from flask_login import current_user
from flask_security import auth_required, roles_required

from application.models.books import Sections, Books
from application.models.user_book_activity import UserActivity
from application.models.users import Users


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
        