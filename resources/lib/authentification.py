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
        self.clientIsPlaying = ''
        self.nom = ""
        self.prenom = ""
        self.availableDays = ""
        self.permitUser = False
        self.oConfig = cConfig()

    def checkCredentials(self):
        self.oConfig.log('checkCredentials')
        attempt = 0
        self.clientCode = self.oConfig.getSetting('tvWatchCode')
        showNofication = False
        while not self.isCodeValid():
            self.oConfig.log("Client code: " + self.clientCode)
            self.clientCode = self.oConfig.createDialogNum(util.VSlang(30421))
            showNofication = True
            attempt += 1
            if self.clientCode == '' or attempt >= 3:
                return False
        if self.permitUser:
            return True
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
                self.oConfig.setSetting('tvWatchCode', self.clientCode)
                cDb().insert_clientID(str(i[0]))
                self.prenom = i[1]
                self.nom = i[2]
                self.clientExpDate = i[4]
                self.clientIsPlaying = i[5]
                # self.oConfig.log('isCodeValid OK !')
                return True
        if content == []:
            self.permitUser = True
            self.oConfig.log('isCodeValid ERROR')
            self.oConfig.log('permit the client to use the app')
            return True
        self.oConfig.log('isCodeValid NOK !')
        return False

    def isExpirationDateValid(self):
        from datetime import date
        d,m,y = self.clientExpDate.replace(" ", "").split("/")
        userExpDate = date(int(y), int(m), int(d))
        dateOfToday = self.oConfig.getCurrentDate()
        if userExpDate < dateOfToday:
            self.oConfig.log('isExpirationDateValid NOK !')
            cGui().showInfo("Authentification", util.VSlang(30450), 3)
            return False
        else:
            # self.oConfig.log('isExpirationDateValid OK !')
            self.availableDays = str((userExpDate - dateOfToday).days)
            self.oConfig.setSetting('expirationDate', self.availableDays)
            return True

    def accountNotInUse(self):
        res = True
        isPlaying = self.oConfig.getSetting('isPlaying')
        if isPlaying == '':
            self.oConfig.setSetting('isPlaying', self.clientIsPlaying)
        else:
            if int(self.clientIsPlaying) > int(isPlaying):
                self.oConfig.setSetting('isPlaying', self.clientIsPlaying)
                self.oConfig.log('accountNotInUse NOK !')
                cGui().showInfo("Authentification", util.VSlang(30437), 3)
                res = False
        return res
