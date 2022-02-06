import traceback
from flask import current_app, request, session
# from common.app_defaults import process_input, response_factory
from common.custom_exception import CustomException
from common.request_response_utils import proccess_input, response_factory
from backend import all_routes



class GenericEndpoint(object):
    routes = []
    dao = None
    upload_operations = None
    upload_method = None
    operation_parameters = ['uuid', 'input']

    @classmethod
    def generic_operation(cls, operation, **kwargs):
        error = result = input = options = None
        code = 3
        method = getattr(cls.dao, operation)



        try:
            if request.method == 'POST':
                input = proccess_input(request)
            
                # arguments = []
                # for argument in cls.operation_parameters:
                #     arguments.append(vars()[argument])
                kwargs = kwargs | input # Merge with input
                
            result = method(kwargs)

            if options and any(operation == op for op in cls.upload_operations):
                if options.get('files'):
                    cls.upload_method(uuid, result['uuid'], options)
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
        return cls.response_operation(response)

    @classmethod
    def initialize_routes(cls):
        
        for route in cls.routes:
            all_routes.append(route)
            print('adding', route['route'])
            current_app.add_url_rule(route['route'], route['route'], cls.generic_operation, defaults={
                                    'operation': route['operation']}, **{'methods': [route['method']]})

    @classmethod
    def response_operation(cls, response):
        return response
