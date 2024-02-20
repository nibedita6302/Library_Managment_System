from .users import UserRegister

def config_all_resource(api):
    user_api(api)

def user_api(api):
    api.add_resource(UserRegister, "/user-registration")