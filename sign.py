# -*- coding: utf-8 -*-
# Author:w k

def gen_sign(appid, secret_key):
    if not appid or not secret_key:
        return -1
    expired = 0
    now = int(time.time())
    rdm = random.randint(0, 999999999)
    plain_text = 'a=' + str(appid) + '&e=' + str(expired) + '&t=' + str(now) + '&r=' + str(rdm)
    bin = hmac.new(secret_key.encode(), plain_text.encode(), hashlib.sha1)
    s = bin.hexdigest()
    s = binascii.unhexlify(s)
    s = s + plain_text.encode('ascii')
    signature = base64.b64encode(s).rstrip()
    return signature

GAME_APPID = '18931'
GAME_SECRET_KEY = 'gY3cwxdkwXmuR4z2gmpmzChqVZJ'
a = gen_sign(GAME_APPID, GAME_SECRET_KEY)
print(a)