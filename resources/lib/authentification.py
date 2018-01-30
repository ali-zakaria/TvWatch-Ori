#-*- coding: utf-8 -*-
# Venom.
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.config import cConfig
from resources.lib import util
import csv
import base64
from datetime import date
import hashlib, uuid

class cAuthentification:

    SITE_NAME = 'cAuthentification'

    code = ''

    def checkCredentials(self):
        cConfig().log('checkCredentials')
        attempt = 0
        self.code = cConfig().getSetting('vstream_code')
        while self.isCodeValid(self.code) == False:
            self.code = cConfig().createDialogNum(util.VSlang(30421))
            attempt += 1
            if self.code == '' or attempt >= 3:
                return False
        cConfig().setSetting('vstream_code', self.code)
        return True

    def isCodeValid(self, code):
        status = False
        with open('Book1.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if self.check_password(code, row['code']):
                    cConfig().log('Code OK !')
                    status = self.isExpirationDateValid(row['expiration_date'])
                    break
        return status

    def isExpirationDateValid(self, userDate):
        status = True
        d,m,y = userDate.replace(" ", "").split("/")
        userExpDate = date(int(y), int(m), int(d))
        if userExpDate < date.today():
            status = False
        return status

    def downloadCSV(self):
        download = 1

    def set_password(self, raw_password):
        salt = uuid.uuid4().hex
        hsh = hashlib.sha1(raw_password + salt).hexdigest()
        enc_password = '%s$%s' % (salt, hsh)
        return enc_password

    def check_password(self, raw_password, enc_password):
        salt,hsh = enc_password.split("$")
        return hsh == hashlib.sha1(raw_password + salt).hexdigest()
