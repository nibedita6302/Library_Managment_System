from application.database import db 
from security import datastore
from .credentials import hash_password
from application.models.users import Users, Role 

def create_default_data(librarian_email, yourname):
    # create roles
    datastore.find_or_create_role(id=1, name='librarian', description='CRUD on Books and Sections.')
    datastore.find_or_create_role(id=2, name='user', description='Issue books and buy book PDF')
    db.session.commit()  
    if not datastore.find_user(email=librarian_email):
        #creating the only Librarian
        lib1 = datastore.create_user(email=librarian_email, name=yourname, password=hash_password(''))
        datastore.add_role_to_user(lib1, 'librarian')
    db.session.commit() 
