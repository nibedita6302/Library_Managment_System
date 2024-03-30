from .users import UserRegister, UserProfile
from .sections import ManageSections, DisplaySections
from .authors import AuthorManagement
from .books import ManageBook, Books_in_Section, Download_Book, Read_Book
from .reviews import UserReview
from .search import SearchBooks
from .user_book_activity import Issue_Book_Request, PendingIssues, UserStats
from .librarian import LibrarianAnalytics, Issue_Request_Approval

def config_all_resource(api):
    user_api(api)
    section_api(api)
    author_api(api)
    book_api(api)
    search_api(api)
    review_api(api)
    user_activity_api(api)
    librarian_stats_api(api)

def user_api(api):
    api.add_resource(UserRegister, "/user-registration")
    api.add_resource(UserProfile, "/user/profile", "/user/profile/update", 
                     "/user/profile/delete/<int:confirm>")

def section_api(api):
    api.add_resource(ManageSections, '/section/<int:section_id>', "/section/create", 
                     "/section/update/<int:section_id>", "/section/delete/<int:section_id>")
    api.add_resource(DisplaySections, '/home/sections')

def author_api(api):
    api.add_resource(AuthorManagement, '/author/<int:author_id>', '/author/create', 
                     '/author/update/<int:author_id>', '/author/delete/<int:author_id>/<int:confirm>')

def book_api(api):
    api.add_resource(ManageBook, '/book/<int:book_id>', '/book/create', '/book/update/<int:book_id>',
                     '/book/delete/<int:book_id>')
    api.add_resource(Books_in_Section, '/section/<int:section_id>/books')
    api.add_resource(Download_Book, '/book/buy/<int:issue_id>')
    api.add_resource(Read_Book, '/book/read/<int:issue_id>')

def review_api(api):
    api.add_resource(UserReview, '/book/<int:book_id>/review')

def search_api(api):
    api.add_resource(SearchBooks, '/search')

def user_activity_api(api):
    api.add_resource(Issue_Book_Request, '/current-issues', '/issue-requests/new/<int:book_id>',
                      '/issue-requests/return/<int:issue_id>', '/test/<int:issue_id>')
    api.add_resource(PendingIssues, '/pending-issues')
    api.add_resource(UserStats, '/user-stats')

def librarian_stats_api(api):
    api.add_resource(LibrarianAnalytics, '/librarian-stats')
    api.add_resource(Issue_Request_Approval, '/issue-requests/approval/<int:book_id>/<int:user_id>',
                     '/issue-requests/revoke/<int:issue_id>')
