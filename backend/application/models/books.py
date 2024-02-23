from datetime import datetime, timedelta
from ..database import db 
from sqlalchemy import Integer, String, Boolean, DateTime, Float, ForeignKey,  Column

## many-to-many relationship table between Authors and Books
AuthorBook = db.Table('author_book',
    Column('b_id', Integer(), ForeignKey('books.b_id', ondelete="CASCADE"), primary_key=True), # books
    Column('a_id',Integer(), ForeignKey('authors.a_id', ondelete="CASCADE"), primary_key=True),  # authors
    Column('read_count',Integer(), nullable=False, default=0),
    Column('bought_count', Integer(), nullable=False, default=0)
)

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
    #relationship
    reviews = db.relationship('Reviews', cascade='all, delete-orphan')
    user_book = db.relationship('UserBook', back_populates='books', cascade='all, delete')

    def __repr__(self) -> str:
        return f"Books - {self.b_id}:{self.b_name}"
    
class Sections(db.Model):
    __tablename__='sections'
    s_id = Column(Integer(), autoincrement=True, primary_key=True)
    s_name = Column(String(), unique=True, nullable=False)
    s_image = Column(String(), unique=True, nullable=False)
    book_count = Column(Integer(), nullable=False, default=0)

    def __repr__(self) -> str:
        return f"Sections - {self.s_id}:{self.s_name}"

class Author(db.Model):
    __tablename__='authors'
    a_id = Column(Integer(), autoincrement=True, primary_key=True)
    a_name = Column(String(), unique=True, nullable=False)   
    about_author = Column(String(), nullable=False)   
    #relationships
    biblography = db.relationship('Books', secondary=AuthorBook, backref='writer')

    def __repr__(self) -> str:
        return f"Authors - {self.a_id}:{self.a_name}"

