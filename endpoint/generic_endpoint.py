import traceback
from typing import Dict
from flask import current_app, request
from common.custom_exception import CustomException
from common.dao_generic import commit, delete
from common.jsonify import jsonify_list
from common.request_response_utils import proccess_input, response_factory
from backend import all_routes
import inspect
from backend import db
from flask import session


class GenericEndpoint(object):

    routes = []

    model = None
    name = ''
    id_field = ''
    prefix = ''
    default_id_field = 'id'
    default_payload_field = ''
    get_one_config = ''
    get_all_config = ''
    delete_config = ''
    create_config = ''
    update_config = ''

    def __init__(self, model, name=None, id_field=None, prefix=None, get_one=None, get_all=None, delete=None, create=None, update=None):

        self.model = model
        self.name = name if name else model.__name__.lower()
        self.id_field = id_field if id_field else self.default_id_field
        self.default_payload_field = f"{self.name}_{self.id_field}"

        # GET-ONE, GET-ALL, CREATE, UPDATE, DELETE AUTOMATIC ENDPOINTS

        get_one_config_default = {'fields': None, 'id_field': self.id_field, 'payload_field': self.id_field, 'route': f'/{self.name}/<{self.id_field}>',
                                  'perm': None, 'method': 'GET', 'operation': self.get_one, 'keyword': f'get-one-{self.name}'}

        get_all_config_default = {'fields': None, 'id_field': None, 'payload_field': None, 'route': f'/{self.name}',
                                  'perm': None, 'method': 'GET', 'operation': self.get_all, 'keyword': f'get-all-{self.name}'}

        delete_config_default = {'fields': None, 'id_field': self.id_field, 'payload_field': self.id_field, 'route': f'/{self.name}',
                                 'perm': None, 'method': 'DELETE', 'operation': self.delete, 'keyword': f'delete-{self.name}', 'check_owner': None}

        create_config_default = {'fields': None, 'id_field': self.id_field, 'payload_field': self.id_field, 'route': f'/{self.name}', 'create_fields': None,
                                 'perm': None, 'method': 'POST', 'operation': self.create, 'keyword': f'create-{self.name}', 'children': None, 'children_params': None, 'children_field': None}

        update_config_default = {'fields': None, 'id_field': self.id_field, 'payload_field': self.id_field, 'route': f'/{self.name}', 'update_fields': None,
                                 'perm': None, 'method': 'PUT', 'operation': self.update, 'keyword': f'update-{self.name}', 'children': None, 'children_params': None, 'children_field': None}

        if get_one:
            g1 = self.merge_dict(get_one, get_one_config_default)
            self.get_one_config = g1
            self.routes.append(g1)

        if get_all:
            g2 = self.merge_dict(get_all, get_all_config_default)
            self.get_all_config = g2
            self.routes.append(g2)

        if delete:
            g3 = self.merge_dict(delete, delete_config_default)
            self.delete_config = g3
            self.routes.append(g3)

        if create:
            g4 = self.merge_dict(create, create_config_default)
            self.create_config = g4
            self.routes.append(g4)

        if update:
            g5 = self.merge_dict(update, update_config_default)
            self.update_config = g5
            self.routes.append(g5)

    def merge_dict(self, dict: Dict, default_dict: Dict):
        if not dict:
            return default_dict

        else:
            new_dict = {}
            for k in default_dict:
                if dict.get(k):
                    new_dict[k] = dict[k]
                else:
                    new_dict[k] = default_dict[k]

        return new_dict

    def get_one(self, get):

        id_field = self.get_one_config.get('id_field', self.id_field)
        payload_field = self.get_one_config.get(
            'payload_field', self.default_payload_field)
        fields = self.get_one_config.get('fields', None)

        model_ = self.model.query.filter(
            getattr(self.model, id_field) == get[payload_field]).first()

        if fields:
            return model_.to_dict(only=self.get_one_config.get('fields', '*'))
        else:
            return model_.to_dict()

    def get_all(self, get):
        fields = self.get_all_config.get('fields', None)
        if fields:
            return jsonify_list(self.model.query.all(), fields=fields)
        else:
            return jsonify_list(self.model.query.all())

    def delete(self, post):
        id_field = self.delete_config.get('id_field', self.id_field)
        payload_field = self.delete_config.get(
            'payload_field', self.default_payload_field)

        check_owner: dict = self.delete_config.get('check_owner')
        if check_owner:
            owner_key = list(check_owner.keys())[0]
            owner_value = session.get(list(check_owner.values())[0])
            model_ = self.model.query.filter(
                getattr(self.model, id_field) == post[payload_field],
                getattr(self.model, owner_key) == owner_value,
            ).first()

        else:
            model_ = self.model.query.filter(
                getattr(self.model, id_field) == post[payload_field]).first()

        model = None
        if model_:
            model = model_.to_dict()
            delete(model_)
        return model

    def create(self, payload):
        create_fields = self.create_config['create_fields']
        # model_ = string_to_property(payload, self.model(), create_fields)
        model_ = self.set_params(self.model(), create_fields, payload)
        db.session.add(model_)
        db.session.flush()

        children = self.create_config.get('children')
        if children:
            children_params = self.create_config.get('children_params')
            child_field = self.create_config.get('children_field')

            for child in children:
                params = children_params[child.__name__.lower()]

                multi = params.get('MULTI_')
                if multi:
                    p_multi = payload[multi]
                    for entity in p_multi:
                        print('entity', entity)
                        child_ = self.set_params(
                            child(), params, entity, model_)
                        db.session.add(child_)

                else:
                    child_ = self.set_params(child(), params, payload, model_)
                    db.session.add(child_)

            if child_field:
                setattr(model_, child_field, child_)

        db.session.commit()
        return model_.to_dict()

    def update(self, payload):

        id_field = self.update_config.get('id_field', self.id_field)
        payload_field = self.update_config.get(
            'payload_field', self.default_payload_field)
        check_owner: dict = self.update_config.get('check_owner')

        if check_owner:
            owner_key = list(check_owner.keys())[0]
            owner_value = session.get(list(check_owner.values())[0])
            model_ = self.model.query.filter(
                getattr(self.model, id_field) == payload[payload_field],
                getattr(self.model, owner_key) == owner_value,
            ).first()

        else:
            model_ = self.model.query.filter(
                getattr(self.model, id_field) == payload[payload_field]).first()

        update_fields = self.update_config['update_fields']
        model_ = self.set_params(model_, update_fields, payload)

        children = self.update_config.get('children')
        if children:
            children_params = self.update_config.get('children_params')

            for child in children:
                params = children_params[child.__name__.lower()]

                multi = params['MULTI_']
                if multi:
                    p_multi = payload[multi]
                    for entity in p_multi:
                        id_name = params['ID_']
                        id_value = entity[id_name]
                        child_ = child.query.filter(
                            getattr(child, id_name) == id_value).first()

                        child_ = self.set_params(
                            child_, params, entity, model_)

                        db.session.add(child_)

                else:
                    id_name = params['ID_']
                    id_value = entity[id_name]
                    child_ = child.query.filter(
                        getattr(child, id_name) == id_value).first()

                    child_ = self.set_params(child_, params, payload, model_)
                    db.session.add(child_)

        commit(model_)

    def generic_operation(self, operation, **kwargs):
        error = result = input = options = None
        code = 3
        method = operation

        try:
            if request.method != 'GET':
                input = proccess_input(request)

                kwargs = kwargs | input  # Merge with input

            result = method(kwargs)

            code = 1

        except Exception as e:
            traceback.print_exc()
            if isinstance(e, CustomException):
                error = str(e)
            else:
                error = 'GENERIC ERROR'
            code = 3

        response = current_app.response_class(
            response=None, status=200, mimetype='application/json')
        response.data = response_factory(code, {'items': result}, error)
        return self.response_operation(response)

    def initialize_routes(self):

        for route in self.routes:
            if route not in all_routes:
                all_routes.append(route)
                print('adding', route['route'],
                      route['method'], route.get('perm', 'NONE'))
                current_app.add_url_rule(route['route'], route['route'], self.generic_operation, defaults={
                    'operation': route['operation']}, **{'methods': [route['method']]})

    def response_operation(self, response):
        return response

    def route(self, *args):

        def decorator(f):

            method = ''
            if str(inspect.signature(f)) == '(post)':
                method = 'POST'
            else:
                method = 'GET'

            paramPath = args[0] if len(
                args) > 0 else f"/{f.__name__.replace('_','-')}"
            paramPerm = args[1] if len(
                args) > 1 else None

            self.routes.append({'route': paramPath, 'keyword': f.__name__.replace('_', '-'),
                                'method': method, 'operation': f, 'perm': paramPerm})
            return f
        return decorator

    def set_params(self, object, params: dict, payload, parent=None):
        for k, v in params.items():


            if callable(v):
                setattr(object, k, v())

            elif k == 'MULTI_' or k == 'ID_':
                pass

            elif v.startswith('PARENT_'):
                setattr(object, k, getattr(parent, v.replace('PARENT_', '')))

            elif v.startswith('SESSION_'):
                setattr(object, k, session[v.replace('SESSION_', '')])

            else:
                setattr(object, k, payload[v])

        return object
