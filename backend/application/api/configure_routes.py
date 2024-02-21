from .users import UserRegister, UserProfile

def config_all_resource(api):
    user_api(api)

def user_api(api):
    api.add_resource(UserRegister, "/user-registration")
    api.add_resource(UserProfile, "/user/<int:user_id>", "/user/update/<int:user_id>", 
                     "/user/delete/<int:user_id>/<int:confirm>")