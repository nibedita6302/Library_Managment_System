import os
import requests
from datetime import datetime
from flask import send_file
from flask_restful import Resource, fields, marshal
from application.database import db
from flask import request, current_app as app
from flask_login import current_user
from flask_security import auth_required, roles_required

from application.models.users import Users
from application.models.books import Books, Sections, Author
from application.models.reviews import Reviews
from application.models.user_book_activity import UserBook, UserActivity

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
    "total_issue": fields.Integer,
    "total_bought": fields. Integer
}

review_field = {
    "r_id": fields.Integer,
    "b_id": fields.Integer,
    "user_id": fields.Integer,
    "user_name": fields.String,
    "rating": fields.Integer,
    "review": fields.String
}


class ManageBook(Resource): 
    def get(self, book_id):     ## Get book detail by book ID
        book = Books.query.get(book_id)
        if not book:
            return {'message': {'error': 'Book Not Found'}}, 404
        # book_reviews = book.reviews
        book_reviews = db.session.query(Reviews.r_id, Reviews.b_id, Reviews.user_id,
                        Reviews.rating, Reviews.review, Users.name.label('user_name'))\
                        .join(Reviews, Reviews.user_id==Users.id)\
                        .filter(Reviews.b_id==book.b_id).all()
        return {
            "book_details": marshal(book, book_field),
            "reviews": marshal(book_reviews, review_field)
        }, 200

    @auth_required('token')
    @roles_required('librarian')
    def post(self):                              ## Create New book
        formData = request.form.to_dict()
        if len(formData)==9:
            if (not Sections.query.get(formData['s_id'])) or (not Author.query.get(formData['a_id'])):
                return {'message': {'error': 'Section or Author Not Found'}}, 404   
            ## Convert Date from String to DateTime type
            formData['date_published'] = datetime.strptime(formData['date_published'], "%d/%m/%Y")
            ## PDF price > 0
            if int(formData['pdf_price'])<=0:
                return {'message': {'error': 'Download Price should be greater than 0'}}, 400
            
            ## Converting file ID to Links
            formData['content_link_view'] = 'https://drive.google.com/file/d/'+formData['content_view_id']+'/view?usp=drive_link'
            formData['content_link_download'] = 'https://drive.google.com/uc?export=download&id='+formData['content_download_id']
            
            ## Delete file ids
            del formData['content_view_id']
            del formData['content_download_id']

            author = Author.query.get(formData['a_id'])     ## Add Author Book relationship
            book = Books(**formData, writer=[author])

            if 'b_image' in request.files:
                print('in image')
                image = request.files['b_image']
                if image.filename != "":
                    extension = '.'+image.filename.split('.')[-1]
                    ## Get ID of last book added to database (+1 - new book ID)
                    lastest_id = Books.query.order_by(Books.b_id.desc()).first()     
                    #print(lastest_id)   
                    if lastest_id:
                        lastest_id = lastest_id.b_id+1
                    else:       ## If first Book - ID=1
                        lastest_id = 1
                    img_path = 'book_image_'+str(lastest_id)+extension  ## Save image name with ID of new book
                    #print(img_path)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER']+'upload/',img_path))
                    book.b_image = img_path 

                    section = Sections.query.get(formData['s_id'])      
                    section.book_count+=1           ## Increment book_count in Section

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
    def delete(self, book_id):  ## Delete book if no issues
        book = Books.query.get(book_id)
        if not book:
            return {'message': {'error': 'Book does not exists'}}, 404
        active_issuers = UserBook.query.filter(UserBook.b_id==book_id, 
                                                UserBook.return_date == None).all()
        if len(active_issuers)>0:
            ## 409 HTTP Code for Conflict with current state of target resource
            return {'message': {
                        'error': 'Cannot delete Book because it still has associated issues.\
                                Please revoke all issues first.'
                    }}, 409   
        ## Remove image 
        os.remove(os.path.join(app.config['UPLOAD_FOLDER']+'upload/', book.b_image))     

        section = Sections.query.get(book.s_id)
        section.book_count-= 1         ## decrement book_count on deletion

        db.session.delete(book)   
        db.session.commit()
        return {'message': {'success': 'Deleted Book'}}, 200

class Books_in_Section(Resource):
    ## Display all books in section
    def get(self, section_id):
        books = Books.query.filter_by(s_id=section_id).all()
        return marshal(books, book_field), 200

## API for downloading books/ buying books
class Download_Book(Resource):
    @auth_required('token')
    @roles_required('user')
    def get(self, issue_id):
        ## Check if Issue is made by current user
        user_book = UserBook.query.filter_by(issue_id=issue_id, user_id=current_user.id).first()
        if not user_book:
            return {'message': {'error': 'Please Issue book to be able to download'}}, 403
        if user_book.return_date is not None:
            return {'message': {'error': 'The book has been returned!'}}, 400
        
        book = Books.query.get(user_book.b_id)
        url = book.content_link_download

        user_actv = UserActivity.query.get(issue_id)
        if book.total_bought is None:
            book.total_bought = 1
        else:
            book.total_bought+=1                    ## Increment Total book bought in Books
        user_book.bought_price = book.pdf_price     ## Add bought price in UserBooks
        user_actv.bought_price = book.pdf_price     ## Add bought price in UserActivity

        user = Users.query.get(current_user.id)      
        user.latest_activity = datetime.now()       ## Set User Activity

        db.session.commit()

        response = requests.get(url)         ## Request for PDF from url
        if response.status_code == 200:
            # if 'application/pdf' in content_type:                ## Check if the response contains a PDF
            with open('static/temp.pdf', 'wb') as f:                ## Save the PDF to a temporary file
                f.write(response.content)

            return send_file('static/temp.pdf', as_attachment=True, download_name=f'{book.b_name}.pdf')
        return {"message":{'error':f'Unable to download PDF, error status {response.status_code}'}}, 500

## API for only reading books
class Read_Book(Resource):
    @auth_required('token')
    @roles_required('user')
    def get(self, issue_id):                        ## Read Book Only
        user_book = UserBook.query.get(issue_id)
        if (user_book is None) or (user_book.user_id!=current_user.id):
            return {'message':{'error':'This book is not issued by you, yet.'}}, 403
        if user_book.return_date is not None:
            return {'message':{'error':'The book has been returned!'}}, 400
        book = Books.query.get(user_book.b_id)
        user = Users.query.get(current_user.id)      
        user.latest_activity = datetime.now()       ## Set User Activity
        db.session.commit()
        return {'content_link_view': book.content_link_view}, 200
