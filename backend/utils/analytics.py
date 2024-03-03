from application.database import db

from application.models.user_book_activity import UserActivity
from application.models.users import Users        

def section_distribution_user(user_id):
    ## Section Wise Distribution - Book Reads
    section_count = db.session.query(UserActivity.section_name, db.func.count().label('count'))\
                    .filter(UserActivity.user_id==user_id)\
                    .group_by(UserActivity.section_name).all()
    return section_count

def fav_author(user_id):
    ## Favourite Author
    fav_author = db.session.query(UserActivity.author_name, db.func.count().label('count'))\
                    .filter(UserActivity.user_id==user_id)\
                    .group_by(UserActivity.author_name).all()
    return fav_author

def user_ranking():
    ## Ranking in different book reads (top 3 & current user rank)
    ranking = db.session.query(Users.name)\
                .join(UserActivity, Users.id==UserActivity.user_id)\
                .group_by(UserActivity.user_id)\
                .order_by(db.func.count().desc()).all()
    return ranking