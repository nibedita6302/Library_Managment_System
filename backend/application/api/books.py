import os
from datetime import datetime
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
    "content_link_view": fields.String,
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
        }, 200

    @auth_required('token')
    @roles_required('librarian')
    def post(self):             ## Create New book
        formData = request.form.to_dict()
        if len(formData)==9:
            if (not Sections.query.get(formData['s_id'])) or (not Author.query.get(formData['a_id'])):
                return {'message': {'error': 'Section or Author Not Found'}}, 404   
            ## Convert Date form String to DateTime type
            formData['date_published'] = datetime.strptime(formData['date_published'], "%d/%m/%Y")
            ## PDF price > 0
            if int(formData['pdf_price'])<=0:
                return {'message': {'error': 'Download Price should be greater than 0'}}, 400
            
            author = Author.query.get(formData['a_id'])     ## Add Author Book relationship
            book = Books(**formData, writer=[author])

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

    @auth_required('token')
    @roles_required('librarian')
    def put(self, book_id):     ## Update Book
        formData = request.form.to_dict()
        book = Books.query.get(book_id)

        ## Check if atleast one field is updated
        if len(formData)==0 and 'b_image' not in request.files:
            return {'message': {'error': 'Atleast one field is compulsory'}}, 400
        
        ## set updated values
        for col in Books.__table__.columns:
            if col.name in formData:
                ## Check if valid Author or Section
                if col.name in ['s_id', 'a_id']: 
                    if (not Sections.query.get(formData[col.name])):
                        return {'message': {'error': 'Section or Author Not Found'}}, 404   
                    elif col.name == 'a_id':
                        author = Author.query.get(formData['a_id'])     ## Add Author Book relationship
                        print(author)
                        book.writer = [author]
                ## PDF price greater than 0
                if col.name=='pdf_price' and int(formData[col.name])<=0:
                    return {'message': {'error': 'Download Price should be greater than 0'}}, 400
                if col.name == 'date_published':
                    formData['date_published'] = datetime.strptime(formData['date_published'], "%d/%m/%Y")
                setattr(book,col.name,formData[col.name])

        if 'b_image' in request.files:
                image = request.files['b_image']
                if image.filename != "":
                    img_path = book.b_image
                    image.save(os.path.join(app.config['UPLOAD_FOLDER']+'upload/',img_path))
                    book.b_image = img_path 

        db.session.commit()
        return {'message': {'success': 'Book Update Successfull!'}}, 200

    @auth_required('token')
    @roles_required('librarian')
    def delete(self, book_id, confirm):  ## Delete book if no issues
        if confirm:
            book = Books.query.get(book_id)
            issuers = book.user_book
            if len(issuers)>0:
                ## 409 HTTP Code for Conflict with current state of target resource
                return {'message': {
                            'error': 'Cannot delete Book because it still has associated issues. Please revoke all issues first.'
                        }}, 409   
            ## Remove image 
            os.remove(os.path.join(app.config['UPLOAD_FOLDER']+'upload/', book.b_image))             
            db.session.delete(book)   
            db.session.commit()
            return {'message': {'success': 'Deleted Book'}}, 200
        else:
            return {'message': {'success': 'Canceled Delete'}}, 200 

class Books_in_Section(Resource):
    ## Display all books in section
    def get(self, section_id):
        books = Books.query.filter_by(s_id=section_id).all()
        return marshal(books, book_field), 200

## API for downloading books
class Download_Book(Resource):
    @auth_required('token')
    @roles_required('user')
    def get(self, issue_id):
        ir1 = UserBook.query.get(issue_id)
        if not ir1:
            return {'message': {'error': 'Please Issue book to be able to download'}}, 403   
        book = Books.query.get(ir1.b_id)
        book.total_bought+=1
        ir1.bought_price = book.pdf_price
        db.session.commit()
        return {'content_link_download':book.content_link_download}, 200 
    
## API for only reading books
class Read_Book(Resource):
    @auth_required('token')
    @roles_required('user')
    def get(self, issue_id):         ## Read Book Only
        ir1 = UserBook.query.get(issue_id)
        if (ir1 is None) or (ir1.user_id!=current_user.id):
            return {'message':{'error':'This book is not issued by you, yet.'}}, 400
        if ir1.return_date is not None:
            return {'message':{'error':'The book has already been returned!'}}, 400
        book = Books.query.get(ir1.b_id)
        return {'content_link_view': book.content_link_view}, 200