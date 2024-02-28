import os
from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from security import datastore
from flask import request, jsonify, current_app as app
from flask_login import current_user
from flask_security import auth_required, roles_required

from application.models.books import Books, Sections, Author
from application.models.user_book_activity import UserBook

book_field = {
    "b_id": fields.Integer,
    "s_id": fields.Integer,
    "a_id": fields.Integer,
    "b_name": fields.String,
    "b_image": fields.String,
    "pdf_price": fields.Float,
    "date_published": fields.DateTime,
    "publisher": fields.String,
    "summary": fields.String,
    "content_link": fields.String,
    "total_issue": fields.Integer,
    "total_bought": fields. Integer
}

review_field = {
    "r_id": fields.Integer,
    "b_id": fields.Integer,
    "user_id": fields.Integer,
    "rating": fields.Integer,
    "review": fields.String
}


class ManageBook(Resource): 
    def get(self, book_id):     ## Get book detail by book ID
        book = Books.query.get(book_id)
        if not book:
            return {'message': {'error': 'Book Not Found'}}, 404
        book_reviews = book.reviews

        return {
            "book_details": marshal(book, book_field),
            "reviews": marshal(book_reviews, review_field)
        }


    def post(self):             ## Create New book
        formData = request.form.to_dict()
        if len(formData)==8:
            if (not Sections.query.get(formData['s_id'])) or (not Author.query.get(formData['a_id'])):
                return {'message': {'error': 'Section or Author Not Found'}}, 404    
            book = Books(**formData)
            if 'b_image' in request.files:
                image = request.files['b_image']
                if image.filename != "":
                    extension = '.'+image.filename.split('.')[-1]
                    ## Get ID of last book added to database (+1 - new book ID)
                    lastest_id = Books.query.order_by(Books.s_id.desc()).first()        
                    if lastest_id:
                        lastest_id = lastest_id.b_id+1
                    else:       ## If first Book - ID=1
                        lastest_id = 1
                    img_path = 'book_image_'+str(lastest_id)+extension       ## Save image name with ID of new book
                    image.save(os.path.join(app.config['UPLOAD_FOLDER']+'upload/',img_path))
                    book.b_image = img_path 

                    db.session.add(book)
                    db.session.commit()
                    return {'message': {'success': 'New Book Created!'}}, 200
        return {'message': {'error': 'All fields are compulsory.'}}, 400


    def put(self, book_id):     ## Update Book
        pass 

    def delete(self, book_id):  ## Delete book if no issues
        pass 


class Books_in_Section(Resource):
    ## Display all books in section
    def get(self, section_id):
        pass