from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from security import datastore
from flask import request, jsonify, current_app as app
from flask_login import current_user
from flask_security import auth_required, roles_required

from application.models.books import Books
from application.models.reviews import Reviews
from application.models.user_book_activity import UserBook

class UserReview(Resource):
    @auth_required('token')
    @roles_required('user')
    def post(self, book_id):
        book = Books.query.get(book_id)
        if not UserBook.query.filter_by(user_id = current_user.id, b_id=book_id, return_date=None).first():
            return {'message': {'error': 'Please Issue book to write review'}}, 403   
        jsonData = request.get_json()
        if len(jsonData)!=2 or jsonData['review']=='':
            return {'message': {'error': 'All fields are compulsory.'}}, 400
        if Reviews.query.filter_by(user_id=current_user.id, b_id=book_id).first():
            return {'message': {'error': 'Your review already exists'}}, 400
        if 1<=jsonData['rating']<=5 :
            review = Reviews(**jsonData, user_id=current_user.id, b_id=book_id)
        else:
            return {'message': {'error': 'Rating must be inbetween 1 and 5'}}, 400
        db.session.add(review)
        db.session.commit()
        return {'message': {'success': 'Added review successfully'}}, 200
