
from common.generic_endpoint import GenericEndpoint
from datatabase.dao import dao_user as dao_user

class UserEndpoint(GenericEndpoint):
    routes = [
        {'route': '/get-my-user', 'method': 'GET','operation': 'get_my_user'},
        {'route': '/update-my-user', 'method': 'POST','operation': 'update_my_user'},
        {'route': '/get-users', 'method': 'GET','operation': 'get_users'},
        {'route' : '/register', 'method' : 'POST', 'operation' : 'register'},
        {'route' : '/login', 'method' : 'POST', 'operation' : 'login'},
        {'route' : '/logged-in', 'method' : 'GET', 'operation' : 'logged_in'},
        {'route' : '/get-roles', 'method' : 'GET', 'operation' : 'get_roles'},
        {'route' : '/logout', 'method' : 'GET', 'operation' : 'logout'},
    ]

    dao = dao_user
    operation_parameters = ['input']
    # upload_operations = ['insert_pet', 'update_pet']
    # upload_method = upload_pet_photos
