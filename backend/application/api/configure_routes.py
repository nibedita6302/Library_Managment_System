from users import Login, Logout

def config_all_resource(api):
    user_api(api)

def user_api(api):
    api.add_resource(Login, "/login")
    api.add_resource(Logout, "/logout")