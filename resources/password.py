#-*- coding: utf-8 -*-
# Venom.
# https://github.com/Kodi-vStream/venom-xbmc-addons
#

import hashlib, uuid
import random

def set_password(raw_password):
    salt = uuid.uuid4().hex
    hsh = hashlib.sha1(raw_password + salt).hexdigest()
    enc_password = '%s$%s' % (salt, hsh)
    return enc_password

def check_password(raw_password, enc_password):
    salt,hsh = enc_password.split("$")
    return hsh == hashlib.sha1(raw_password + salt).hexdigest()

raw_password = random.randint(1511000000, 1511999999)
enc_password = set_password(str(raw_password))

print raw_password
print enc_password
