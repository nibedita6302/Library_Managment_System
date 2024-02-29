from datetime import datetime, timedelta
from ..database import db 
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Integer, String, Boolean, DateTime, Float, ForeignKey,  Column, CheckConstraint

## Stores all Issue Requests
## Removes row once issue is accepted or rejected
class IssueRequest(db.Model):
    __tablename__='issue_request'
    # req_id = Column(Integer(), autoincrement=True, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'), primary_key=True)  # users
    b_id = Column(Integer(), ForeignKey('books.b_id'), primary_key=True) # books
    status = Column(Integer(), nullable=False, default=2)

    __table_args__ = (
        ## 0 -> Rejected, 1 -> Accepted, 2 -> Pending
        CheckConstraint('status IN (0,1,2)', name='issue_status'),
    )

## many-to-many relationship table between Users and Books
## Same book can be issued by the same user multiple times (after being returned)
class UserBook(db.Model): 
    __tablename__='user_book'
    issue_id = Column(Integer(), autoincrement=True, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'), nullable=False)  # users
    b_id = Column(Integer(), ForeignKey('books.b_id'), nullable=False) # books
    issue_date = Column(DateTime(), default=datetime.now(), nullable=False)
    due_date = Column(DateTime(), default=datetime.now()+timedelta(days=7), nullable=False)
    return_date = Column(DateTime())
    # read_count = Column(Integer(), nullable=False, default=0)
    bought_price = Column(Integer(), nullable=False, default=0)
    #relationships 
    issuer = db.relationship('Users', back_populates='user_book', cascade='all, delete')
    books = db.relationship('Books', back_populates='user_book', cascade='all, delete')

    def __repr__(self) -> str:
        return f"User-Book - {self.b_id}:{self.users_id}" 

## Book info that user issue
## One-to-Many relationship with Users
class UserActivity(db.Model):
    __tablename__='user_activity'
    actv_id = Column(Integer(), autoincrement=True, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'), nullable=False)  # users
    book_name = Column(String(), nullable=False)
    section_name = Column(String(), nullable=False)
    author_name = Column(String(), nullable=False)
    issue_date = Column(DateTime(), nullable=False)
    return_date = Column(DateTime())
    bought_price = Column(Integer(), nullable=False, default=0)

    def __repr__(self) -> str:
        return f"UserActivity - {self.b_id}:{self.users_id}" 
    
    @hybrid_property
    def month_name(self):
        return datetime.strftime(self.issue_date, "%B")
