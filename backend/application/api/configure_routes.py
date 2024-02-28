from .users import UserRegister, UserProfile
from .sections import ManageSections, SectionAnalytics, DisplaySections
from .authors import AuthorManagement
from .books import ManageBook, Books_in_Section, Download_Book
from .reviews import UserReview
from .search import SearchBooks

def config_all_resource(api):
    user_api(api)
    section_api(api)
    author_api(api)
    book_api(api)

def user_api(api):
    api.add_resource(UserRegister, "/user-registration")
    api.add_resource(UserProfile, "/user/<int:user_id>", "/user/update/<int:user_id>", 
                     "/user/delete/<int:user_id>/<int:confirm>")

def section_api(api):
    api.add_resource(ManageSections, '/section/<int:section_id>', "/section/create", 
                     "/section/update/<int:section_id>", "/section/delete/<int:section_id>/<int:confirm>")
    api.add_resource(DisplaySections, '/home/sections')

def author_api(api):
    api.add_resource(AuthorManagement, '/author/<int:author_id>', '/author/create', 
                     '/author/update/<int:author_id>', '/author/delete/<int:author_id>/<int:confirm>')

def book_api(api):
    api.add_resource(ManageBook, '/book/<int:book_id>', '/book/create', '/book/update/<int:book_id>',
                     '/book/delete/<int:book_id>/<int:confirm>')
    api.add_resource(Books_in_Section, '/section/<int:section_id>/books')
    api.add_resource(Download_Book, '/book/buy/<int:book_id>')

def review_api(api):
    api.add_resource(UserReview, '/book/<int:book_id>/review')

def search_api(api):
    api.add_resource(SearchBooks, '/search')

from .test import Test
def test_api(api):
    api.add_resource(Test, "/tests-1/<int:num>", "/tests/<int:num>/<int:add>", endpoint="test-api")