from typing import List


def jsonify_list(list: List, fields=None):
    result = []
    for item in list:

        if fields:
            item_json = item.to_dict(only=fields)

        else:
            item_json = item.to_dict()

        result.append(item_json)

    return result
