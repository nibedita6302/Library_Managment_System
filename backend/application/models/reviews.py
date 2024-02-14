from ..database import db
from sqlalchemy import Integer, String, Boolean, ForeignKey, Column, relationship

class Reviews(db.Model):
    r_id = Column(Integer(), autoincrement=True, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id')),  # users
    b_id = Column(Integer(), ForeignKey('books.b_id')), # books
    rating = Column(Integer())
    review = Column(String(100))

    def __repr__(self) -> str:
        return f"Reviews - User:{self.user_id} Book:{self.b_id} Rating:{self.rating}"
    

