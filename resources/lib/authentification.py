#-*- coding: utf-8 -*-
# Primatech.
# https://github.com/Kodi-TvWatch/primatech-xbmc-addons
#
from resources.lib.config import cConfig
from resources.lib import util
from resources.lib.mySqlDB import cMySqlDB
from resources.lib.db import cDb
from resources.lib.gui.gui import cGui
import hashlib, uuid
import xbmc

class cAuthentification:

    def __init__(self):
        self.clientCode = '0000'
        self.clientExpDate = '01/01/1970'
        self.clientIsPlaying = 'True'
        self.nom = ""
        self.prenom = ""
        self.availableDays = ""

    def checkCredentials(self, force = False):
        cConfig().log('checkCredentials')
        attempt = 0
        self.clientCode = cConfig().getSetting('tvWatchCode')
        showNofication = False
        while not self.isCodeValid() or force:
            cConfig().log("Client code: " + self.clientCode)
            self.clientCode = cConfig().createDialogNum(util.VSlang(30421))
            showNofication = True
            attempt += 1
            if self.clientCode == '' or attempt >= 3:
                return False
        if self.isExpirationDateValid() and self.accountNotInUse():
            if showNofication:
                cGui().showInfo(util.VSlang(30306) % self.prenom, util.VSlang(30442) % self.availableDays, 7)
            return True
        else:
            return False

    def isCodeValid(self):
        content = cMySqlDB().getContent()
        for i in content:
            salt, hsh = i[3].split("$")
            if hashlib.sha1(self.clientCode + salt).hexdigest() == hsh:
                cConfig().setSetting('tvWatchCode', self.clientCode)
                cDb().insert_clientID(str(i[0]))
                self.prenom = i[1]
                self.nom = i[2]
                self.clientExpDate = i[4]
                self.clientIsPlaying = i[5]
                # cConfig().log('isCodeValid OK !')
                return True
        cConfig().log('isCodeValid NOK !')
        return False

    def isExpirationDateValid(self):
        from datetime import date
        d,m,y = self.clientExpDate.replace(" ", "").split("/")
        userExpDate = date(int(y), int(m), int(d))
        dateOfToday = date.today()
        if userExpDate < dateOfToday:
            cConfig().log('isExpirationDateValid NOK !')
            return False
        else:
            # cConfig().log('isExpirationDateValid OK !')
            self.availableDays = str((userExpDate - dateOfToday).days)
            return True

    def accountNotInUse(self):
        if self.clientIsPlaying == "False":
            # cConfig().log('accountNotInUse OK !')
            return True
        else:
            cConfig().log('accountNotInUse NOK !')
            cGui().showInfo("Authentification", util.VSlang(30437), 3)
            # self.checkCredentials(True)
            # xbmc.sleep(3000)
            return False
