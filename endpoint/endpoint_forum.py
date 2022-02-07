from common.generic_endpoint import GenericEndpoint
from datatabase.dao import dao_forum as dao_forum


class ForumEndpoint(GenericEndpoint):
    routes = [
        {'route': '/get-forums', 'method': 'GET', 'operation': 'get_forums'},
        {'route': '/manage/forum/<fuuid>', 'method': 'GET', 'operation': 'get_forum'},
        {'route': '/manage/forum/create-forum', 'method': 'POST', 'operation': 'create_forum'},
        {'route': '/manage/forum/<fuuid>/forum_acl', 'method': 'POST', 'operation': 'get_forum_acl'},
        {'route': '/manage/forum/<fuuid>/update', 'method': 'POST', 'operation': 'update_forum'},
        {'route': '/manage/forum/<fuuid>/delete', 'method': 'POST', 'operation': 'delete_forum'},
    ]

    dao = dao_forum
    operation_parameters = ['input']
    # upload_operations = []
    # upload_method = ''