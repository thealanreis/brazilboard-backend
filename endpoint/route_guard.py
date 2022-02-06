from flask import g
import json
from flask import request, Blueprint, session
from sqlalchemy import all_
from backend import all_routes
from common.custom_exception import CustomException
from common.request_response_utils import response_factory
from datatabase.dao.dao_user import get_acl_entry
from traceback import print_exc
from datatabase.model.forum import Forum

from datatabase.model.forum_acl import ForumACL
# from datatabase.model.moderator_acl import ModeratorACL
route_guard_bp = Blueprint('route_guard', __name__)


@route_guard_bp.before_app_request
def route_guard_route():

    url = str(request.url_rule)

    if session.get('role_name') == 'ADMIN':
        g.acl = ['read_topic', 'write_topic', 'edit_topic', 'delete_topic',
                 'write_post', 'edit_post', 'delete_post',
                 'write_pool', 'edit_pool', 'delete_pool',
                 'edit_any_topic', 'delete_any_topic', 'edit_any_post', 'delete_any_post']

    # if session.get('role_name') == 'MODERATOR':
    #     user_id = session.get('id')
    #     moderator_ = ModeratorACL.query.filter_by(user_id=id).first()

    #     if moderator_:
    #         g.acl = ['read_topic', 'write_topic', 'edit_topic', 'delete_topic',
    #                  'write_post', 'edit_post', 'delete_post',
    #                  'write_pool', 'edit_pool', 'delete_pool',
    #                  'edit_any_topic', 'delete_any_topic', 'edit_any_post', 'delete_any_post']

    else:

        try:
            if url.startswith('/manage'):
                if not any(role for role in ['ADMIN'] if role == session.get('role_name')):
                    return response_factory(4, None, None)

            if url.startswith('/forum'):
                match = next(
                    route for route in all_routes if route['route'] == url)
                return enforce_forum_acl(match)

        except Exception as e:
            print_exc()
            return response_factory(4, None, None)

    # print('ALL ROUTES', all_routes)


def enforce_forum_acl(match):
    forum_uuid = request.view_args['forum_uuid']
    role_id = session.get('role_id')
    user_id = session.get('id')

    forum_:Forum = Forum.query.filter_by(uuid=forum_uuid).first()
    
    # moderator_ = ModeratorACL.query.filter_by(
    #     user_id=user_id, forum_uuid=forum_uuid).first()

    if any(user for user in forum_.moderators if user.id == user_id):
        print('moderador')
        g.acl = ['read_topic', 'write_topic', 'edit_topic', 'delete_topic',
                 'write_post', 'edit_post', 'delete_post',
                 'write_pool', 'edit_pool', 'delete_pool',
                 'edit_any_topic', 'delete_any_topic', 'edit_any_post', 'delete_any_post']

    else: 
        perm = match['perm']
        acl_ = get_acl_entry(forum_uuid, role_id, perm)
        print(acl_)

        if acl_ is None:
            return response_factory(4, None, None)

        else:
            g.acl = get_perms(acl_)


@route_guard_bp.after_app_request
def route_guard_route(response):
    if 'acl' in g:
        acl = g.get('acl')
        r = response.get_json()
        r['result']['acl'] = acl
        response.data = json.dumps(r)
    return response


def get_perms(acl: ForumACL):
    perms = []
    for property, value in vars(acl).items():
        if property not in ('_sa_instance_state', 'id', 'role_id', 'forum_uuid') and value:
            perms.append(property)

    return perms

# @route_guard_bp.route('/route-guard', methods=['POST'])
# @jwt_optional
# def route_guard(uuid, role):

#     input, _ = process_input(request)
#     path = input['path']
#     route_permissions = RoutePermission.query.filter_by(type='FRONTEND').all()
#     response = check_permissions(route_permissions, path, uuid, role)

#     if response is None:
#         response = response_factory(1, True, None)

#     return response


# def check_permissions(route_permissions, path, uuid, role):
#     for entry in route_permissions:
#         if path.startswith(getattr(entry, 'url')):
#             csrf.protect()
#             if (uuid is None or role is None) or (all(permission.name != entry.permission.name for permission in get_role_permissions(role))):
#                 return response_factory(4, False, 'Não autorizado')


# @route_guard_bp.route('/menu-entries', methods=['GET'])
# def get_menu_entries():
#     uuid = get_uuid_from_jwt()
#     role = get_role_from_jwt()

#     entries = []

#     if role and uuid:

#         permissions = get_role_permissions(role)
#         entries_ = MenuEntry.query.filter(
#             MenuEntry.permission_id.in_(p.id for p in permissions)).order_by(MenuEntry.index).all()
#         entries = parse_list(entries_)

#     return response_factory(1, entries, None)
