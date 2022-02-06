from crypt import crypt, mksalt, METHOD_BLOWFISH
from hmac import compare_digest as compare_hash

def generate_password_hash(password):
    return crypt(password, mksalt(method=METHOD_BLOWFISH))
    
def password_match(password, dbpassword):
    return compare_hash(crypt(password, dbpassword), dbpassword)