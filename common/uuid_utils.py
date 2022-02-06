import shortuuid

def generate_uuid():
    # return shortuuid.uuid()
    return shortuuid.ShortUUID().random(length=8)