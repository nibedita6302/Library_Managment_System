from ..database import db
from sqlalchemy import Integer, String, ForeignKey, Column

class Reviews(db.Model):
    r_id = Column(Integer(), autoincrement=True, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'), nullable=False)  # users
    b_id = Column(Integer(), ForeignKey('books.b_id'), nullable=False) # books
    rating = Column(Integer(), nullable=False)
    review = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"Reviews - User:{self.user_id} Book:{self.b_id} Rating:{self.rating}"
    

