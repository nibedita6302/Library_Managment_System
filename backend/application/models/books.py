from datetime import datetime, timedelta
from ..database import db 
from sqlalchemy import Integer, String, Boolean, DateTime, Float, ForeignKey,  Column

## many-to-many relationship table between Authors and Books
class AuthorBook(db.Model): 
    __tablename__='author_book'
    b_id = Column(Integer(), ForeignKey('books.b_id'), primary_key=True) # books
    a_id = Column(Integer(), ForeignKey('authors.a_id'), primary_key=True)  # authors
    read_count = Column(Integer(), nullable=False, default=0)
    bought_count = Column(Integer(), nullable=False, default=0)

    def __repr__(self) -> str:
        return f"Author-Book - {self.b_id}:{self.a_id}"
    

## many-to-many relationship table between Users and Books
class UserBook(db.Model): 
    __tablename__='user_book'
    issue_id = Column(Integer(), autoincrement=True, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'), nullable=False)  # users
    b_id = Column(Integer(), ForeignKey('books.b_id'), nullable=False) # books
    issue_date = Column(DateTime(), default=datetime.now(), nullable=False)
    due_date = Column(DateTime(), default=datetime.now()+timedelta(days=7), nullable=False)
    return_date = Column(DateTime())
    read_count = Column(Integer(), nullable=False, default=0)
    bought_count = Column(Integer(), nullable=False, default=0)

    def __repr__(self) -> str:
        return f"User-Book - {self.b_id}:{self.users_id}"

class Books(db.Model):
    __tablename__='books'
    b_id = Column(Integer(), autoincrement=True, primary_key=True)
    s_id = Column(Integer(), ForeignKey('sections.s_id'), nullable=False) # sections
    a_id = Column(Integer(), ForeignKey('authors.a_id'), nullable=False)  # authors
    b_name = Column(String(), nullable=False)
    b_image = Column(String(), unique=True, nullable=False)
    pdf_price = Column(Float(), nullable=False)
    date_published = Column(DateTime(), nullable=False, default=datetime.now())
    publisher = Column(String(), nullable=False)
    summary = Column(String(), nullable=False)
    content_link = Column(String(), nullable=False)
    total_issue = Column(Integer(), nullable=False, default=0)
    total_bought = Column(Integer(), nullable=False, default=0)
    is_deleted = Column(Boolean(), nullable=False, default=False)
    #relationship
    reviews = db.relationship('Reviews', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        deleted = ''
        if self.is_deleted == True:
            deleted = 'deleted'
        return f"Books - {self.b_id}:{self.b_name} {deleted}"
    
class Sections(db.Model):
    __tablename__='sections'
    s_id = Column(Integer(), autoincrement=True, primary_key=True)
    s_name = Column(String(), nullable=False)
    s_image = Column(String(), unique=True, nullable=False)
    book_count = Column(Integer(), nullable=False, default=0)
    # Relationship between Books and Other tables may get disrupted if deleted.
    # Therefore, cannot actually remove sections or books instances.
    # The above is yet to be confirmed!!
    is_deleted = Column(Boolean(), nullable=False, default=False)  

    def __repr__(self) -> str:
        deleted = ''
        if self.is_deleted == True:
            deleted = 'deleted'
        return f"Sections - {self.s_id}:{self.s_name} {deleted}"

class Author(db.Model):
    __tablename__='authors'
    a_id = Column(Integer(), autoincrement=True, primary_key=True)
    a_name = Column(String(), nullable=False)   
    about_author = Column(String(), nullable=False)   
    #relationships
    biblography = db.relationship('Books', secondary=AuthorBook, backref='writer', 
                                  cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"Authors - {self.a_id}:{self.a_name}"

