from typing import List


def string_to_property(o: dict, obj: object, parameters: List):

    for parameter in parameters:
        setattr(obj, parameter, o[parameter])
    
    return obj
    