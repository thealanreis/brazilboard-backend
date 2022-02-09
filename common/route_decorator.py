def route(argument):
    def decorator(function):
        def wrapper(*args, **kwargs):
            print(argument)
            result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator