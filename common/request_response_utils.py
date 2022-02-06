import json
from common.app_defaults import DEFAULT_INPUT_KEY, DEFAULT_RESPONSE_KEYWORD_CODE, DEFAULT_RESPONSE_KEYWORD_ERROR, DEFAULT_RESPONSE_KEYWORD_RESULT

from common.custom_exception import CustomException

def proccess_input(request):

    if request.is_json:
        return request.json

    elif request.form:
        input = json.loads(request.form[DEFAULT_INPUT_KEY])
        input['files'] = request.files

        return input

    else:
        raise CustomException(
            f"Missing required fields [{DEFAULT_INPUT_KEY}]")


def check_required_fields(input_keys, required_keys):

    for key in required_keys:
        if key not in input_keys:
            raise CustomException(
                'Required key [' + key + '] missing from json input')
    return True


def response_factory(code=None, result=None, error=None):
    return json.dumps(
        {DEFAULT_RESPONSE_KEYWORD_CODE: code,
         DEFAULT_RESPONSE_KEYWORD_RESULT: result,
         DEFAULT_RESPONSE_KEYWORD_ERROR: error}
    )
