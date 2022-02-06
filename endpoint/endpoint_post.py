from common.generic_endpoint import GenericEndpoint
from datatabase.dao import dao_post as dao_post


class PostEndpoint(GenericEndpoint):
    routes = [
        {'route': '/forum/<forum_uuid>/topic/<topic_uuid>/post/<post_uuid>',
            'method': 'GET', 'operation': 'get_post', 'perm': 'read_topic'},
        {'route': '/forum/<forum_uuid>/topic/<topic_uuid>/post',
            'method': 'GET', 'operation': 'get_posts', 'perm': 'read_topic'},
        {'route': '/forum/<forum_uuid>/topic/<topic_uuid>/post/create',
            'method': 'POST', 'operation': 'create_post', 'perm': 'write_post'},
        {'route': '/forum/<forum_uuid>/topic/<topic_uuid>/post/<post_uuid>/update',
            'method': 'POST', 'operation': 'update_post', 'perm': 'edit_post'},
        {'route': '/forum/<forum_uuid>/topic/<topic_uuid>/post/<post_uuid>/delete',
            'method': 'POST', 'operation': 'delete_post', 'perm': 'delete_post'},
    ]

    dao = dao_post
    operation_parameters = ['input']
    # upload_operations = []
    # upload_method = ''