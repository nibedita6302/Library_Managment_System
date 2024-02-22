from .users import UserRegister, UserProfile
from .sections import ManageSections, SectionAnalytics, DisplaySections

def config_all_resource(api):
    user_api(api)
    section_api(api)

def user_api(api):
    api.add_resource(UserRegister, "/user-registration")
    api.add_resource(UserProfile, "/user/<int:user_id>", "/user/update/<int:user_id>", 
                     "/user/delete/<int:user_id>/<int:confirm>")

def section_api(api):
    api.add_resource(ManageSections, '/section/<int:section_id>', "/section/create", 
                     "/section/update/<int:section_id>", "/section/delete/<int:section_id>/<int:confirm>")
    api.add_resource(DisplaySections, '/home/sections')

from .test import Test
def test_api(api):
    api.add_resource(Test, "/tests-1/<int:num>", "/tests/<int:num>/<int:add>", endpoint="test-api")