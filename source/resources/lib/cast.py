#-*- coding: utf-8 -*-

from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.util import VSlog, VSlang

import os
import xbmcvfs
import xbmc

DISABLE = "0"
ENABLE  = "1"

class cCast:

    def __init__(self):
        self.oConfig = cConfig()
        self.pfPath = os.path.join(self.oConfig.getUserDataPath(),'playercorefactory.xml')
        if not self.isApplicable():
            return

    def isApplicable(self):
        return xbmc.getCondVisibility("System.Platform.Android")

    def updateCast(self):
        if not self.isApplicable():
            return
        castPlay = self.oConfig.getSetting('castPlay')
        playercorefactoryPath = os.path.join(self.oConfig.getUserDataPath(),'playercorefactory.xml')
        playercorefactoryExists = xbmcvfs.exists(playercorefactoryPath)
        configChanged = False
        if playercorefactoryExists and castPlay == DISABLE:
            xbmcvfs.delete(playercorefactoryPath)
            configChanged = True
        if not playercorefactoryExists and castPlay == ENABLE:
            playercorefactory = os.path.join(self.oConfig.getRootPath(),'playercorefactory.xml')
            try:
                xbmcvfs.copy(playercorefactory, playercorefactoryPath)
                configChanged = True
            except Exception, e:
                self.oConfig.log("updateCast ERROR: " + e.message)
        if configChanged:
            if self.oConfig.createDialogYesNo(VSlang(30454)):
                try:
                    xbmc.executebuiltin("RestartApp")
                except:
                    self.oConfig.log("Can't use RestartApp fonction, call Quit instead")
                    xbmc.executebuiltin("Quit")

    def checkLocalCast(self):
        if not self.isApplicable() or self.oConfig.getSetting('castPlay') == DISABLE:
            return True
        packageName = 'de.stefanpledl.localcast'
        path = self.oConfig.getAddonPath().split("org.xbmc.kodi")[0] + packageName
        if not os.path.exists(path):
            if self.oConfig.createDialogYesNo(VSlang(30455)):
                app = 'com.android.vending'
                intent = 'android.intent.action.VIEW'
                dataType = ''
                dataURI = 'market://details?id=' + packageName

                cmd = 'StartAndroidActivity("%s", "%s", "%s", "%s")' % (app, intent, dataType, dataURI)
                try:
                    xbmc.executebuiltin(cmd)
                except:
                    self.oConfig.log("Can't start Google play App")
                    self.oConfig.error(VSlang(30456))
                return False
        return True
