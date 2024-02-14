from datetime import datetime, timedelta
from ..database import db 
from sqlalchemy import Integer, String, Boolean, DateTime, Float, ForeignKey,  Column, relationship

## many-to-many relationship table between Authors and Books
class AuthorBook(db.Model): 
    __tablename__='author_book'
    b_id = Column(Integer(), ForeignKey('books.b_id'), primary_key=True), # books
    a_id = Column(Integer(), ForeignKey('authors.a_id'), primary_key=True),  # authors
    read_count = Column(Integer(), default=0)
    bought_count = Column(Integer(), default=0)

    def __repr__(self) -> str:
        return f"Author-Book - {self.b_id}:{self.a_id}"
    

## many-to-many relationship table between Users and Books
class UserBook(db.Model): 
    __tablename__='user_book'
    issue_id = Column(Integer(), autoincrement=True, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id')),  # users
    b_id = Column(Integer(), ForeignKey('books.b_id')), # books
    issue_date = Column(DateTime(), default=datetime.now())
    due_date = Column(DateTime(), default=datetime.now()+timedelta(days=7))
    return_date = Column(DateTime(), nullable=True)
    read_count = Column(Integer(), default=0)
    bought_count = Column(Integer(), default=0)

    def __repr__(self) -> str:
        return f"User-Book - {self.b_id}:{self.users_id}"

class Books(db.Model):
    __tablename__='books'
    b_id = Column(Integer(), autoincrement=True, primary_key=True)
    s_id = Column(Integer(), ForeignKey('sections.s_id')), # sections
    a_id = Column(Integer(), ForeignKey('authors.a_id')),  # authors
    b_name = Column(String())
    b_image = Column(String(), unique=True)
    pdf_price = Column(Float())
    date_published = Column(DateTime(), default=datetime.now())
    publisher = Column(String())
    summary = Column(String())
    content_link = Column(String())
    total_issue = Column(Integer(), default=0)
    total_bought = Column(Integer(), default=0)
    is_deleted = Column(Boolean(), default=False)
    #relationship
    reviews = relationship('Reviews', cascade='all, delete-orphans')

    def __repr__(self) -> str:
        deleted = ''
        if self.is_deleted == True:
            deleted = 'deleted'
        return f"Books - {self.b_id}:{self.b_name} {deleted}"
    
class Sections(db.Model):
    __tablename__='sections'
    b_id = Column(Integer(), autoincrement=True, primary_key=True)
    b_name = Column(String())
    b_image = Column(String(), unique=True)
    book_count = Column(Integer(), default=0)
    is_deleted = Column(Boolean(), default=False)

    def __repr__(self) -> str:
        deleted = ''
        if self.is_deleted == True:
            deleted = 'deleted'
        return f"Sections - {self.s_id}:{self.s_name} {deleted}"

class Author(db.Model):
    __tablename__='authors'
    a_id = Column(Integer(), autoincrement=True, primary_key=True)
    a_name = Column(String())   
    about_author = Column(String())   
    #relationships
    biblography = relationship('Books', secondary=AuthorBook, backref='writer', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"Authors - {self.a_id}:{self.a_name}"

