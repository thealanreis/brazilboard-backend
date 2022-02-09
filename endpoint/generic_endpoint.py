import traceback
from flask import current_app, request, session
from sqlalchemy import all_
# from common.app_defaults import process_input, response_factory
from common.custom_exception import CustomException
from common.request_response_utils import proccess_input, response_factory
from backend import all_routes
import inspect

class GenericEndpoint(object):

    routes = []

    def generic_operation(self, operation, **kwargs):
        error = result = input = options = None
        code = 3
        method = operation

        try:
            if request.method == 'POST':
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
                print('adding', route['route'], route['perm'])
                current_app.add_url_rule(route['route'], route['route'], self.generic_operation, defaults={
                    'operation': route['operation']}, **{'methods': [route['method']]})

    def response_operation(self, response):
        return response

    def route(self, *args):

        def decorator(f):

            print('função ' ,inspect.signature(f))
            method = ''

            if str(inspect.signature(f)) == '(post)':
                method = 'POST'
            else:
                method = 'GET'

            paramPath = args[0] if len(
                args) > 0 else f"/{f.__name__.replace('_','-')}"
            paramPerm = args[1] if len(
                args) > 1 else None

            self.routes.append({'route': paramPath,
                                'method': method, 'operation': f, 'perm': paramPerm})
            return f
        return decorator
