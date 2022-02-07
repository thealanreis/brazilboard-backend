from common.generic_endpoint import GenericEndpoint
from datatabase.dao import dao_topic as dao_topic


class TopicEndpoint(GenericEndpoint):
    routes = [
        {'route': '/forum/<fuuid>/topic/<tuuid>', 'method': 'GET',
            'operation': 'get_topic', 'perm': 'read_topic'},
        {'route': '/forum/<fuuid>/topic', 'method': 'GET',
            'operation': 'get_topics', 'perm': 'read_topic'},
        {'route': '/forum/<fuuid>/topic/create',
            'method': 'POST', 'operation': 'create_topic', 'perm': 'write_topic'},
        {'route': '/forum/<fuuid>/topic/<tuuid>/update',
            'method': 'POST', 'operation': 'update_topic', 'perm': 'edit_topic'},
        {'route': '/forum/<fuuid>/topic/<tuuid>/delete',
            'method': 'POST', 'operation': 'delete_topic', 'perm': 'delete_topic'},
    ]

    dao = dao_topic
    operation_parameters = ['input']
    # upload_operations = []
    # upload_method = ''
