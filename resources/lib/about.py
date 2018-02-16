#-*- coding: utf-8 -*-
#Primatech.
from config import cConfig

import urllib, urllib2
import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import sys, datetime, time, os

sLibrary = xbmc.translatePath(cConfig().getAddonPath()).decode("utf-8")
sys.path.append(sLibrary)

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import VSlog

SITE_IDENTIFIER = 'about'
SITE_NAME = 'About'

class cAbout:

    def __init__(self):
        self.oConfig = cConfig()
        self.client_id = '85aab916fa0aa0b50a29'
        self.client_secret = '3276c40a94a9752510326873f2361e7b80df1a8e'

    #retourne True si les 2 fichiers sont present mais pas avec les meme tailles
    def checksize(self, filepath, size):
        res = False
        try:
            if os.path.getsize(filepath) != size:
                res = True
        except (OSError, IOError) as e:
            #fichier n'existe pas
            VSlog("checksize ERROR: " + e.strerror)
        return res

    def getUpdate(self):
        service_time = self.oConfig.getSetting('service_time')
        VSlog("getUpdate")

        #Si pas d'heure indique = premiere install
        if not (service_time):
            #On memorise la date d'aujourdhui
            self.oConfig.setSetting('service_time', str(datetime.datetime.now()))
            #Mais on force la maj avec une date a la con
            service_time = '2000-09-23 10:59:50.877000'

        if (service_time):
            #delay mise a jour
            time_sleep = datetime.timedelta(minutes=10)
            time_now = datetime.datetime.now()
            time_service = self.__strptime(service_time, "%Y-%m-%d %H:%M:%S.%f")
            if (time_now - time_service > time_sleep):
                self.checkupdate()
            else:
                VSlog('Prochaine verification de MAJ le : ' + str(time_sleep + time_service) )
                #Pas besoin de memoriser la date, a cause du cache kodi > pas fiable.
        return

    #bug python
    def __strptime(self, date, format):
        try:
            date = datetime.datetime.strptime(date, format)
        except TypeError:
            date = datetime.datetime(*(time.strptime(date, format)[0:6]))
        return date

    def __checkversion(self):
        service_version = self.oConfig.getSetting('service_version')
        if (service_version):
            version = self.oConfig.getAddonVersion()
            if (version > service_version):
                try:
                    sUrl = 'https://raw.githubusercontent.com/zakaria220/TvWatch/master/changelog.txt'
                    oRequest =  urllib2.Request(sUrl)
                    oResponse = urllib2.urlopen(oRequest)
                    sContent = oResponse.read()
                    self.TextBoxes('Changelog', sContent)
                    self.oConfig.setSetting('service_version', str(self.oConfig.getAddonVersion()))
                    return
                except:
                    self.oConfig.error("%s,%s" % (self.oConfig.getlanguage(30205), sUrl))
                    return
        else:
            self.oConfig.setSetting('service_version', str(self.oConfig.getAddonVersion()))
            return

    def getRootPath(self, folder):
        sMath = self.oConfig.getAddonPath().decode("utf-8")
        sFolder = os.path.join(sMath , folder)

        # xbox hack
        sFolder = sFolder.replace('\\', '/')
        return sFolder


    def resultGit(self):
        try:    import json
        except: import simplejson as json

        try:
            sRequest = '?client_id=' + self.client_id + '&client_secret=' + self.client_secret
            sUrl = 'https://api.github.com/repos/zakaria220/TvWatch/contents'
            oRequestHandler = cRequestHandler(sUrl + sRequest)
            sHtmlContent = oRequestHandler.request()
            result = json.loads(sHtmlContent)

            for i in result:
                try:
                    if i['type'] == "dir":
                        sUrl = 'https://api.github.com/repos/zakaria220/TvWatch/contents/'
                        sUrl += i['path']
                        oRequestHandler = cRequestHandler(sUrl + sRequest)
                        sHtmlContent = oRequestHandler.request()
                        result += json.loads(sHtmlContent)
                except:
                    pass
        except Exception, e:
            VSlog("resultGit ERROR: "+ e.message)
            return False
        return result


    def checkupdate(self):
        VSlog("checkupdate")
        version = self.oConfig.getAddonVersion()
        try:
            sRequest = '?client_id=' + self.client_id + '&client_secret=' + self.client_secret
            sUrl = 'https://raw.githubusercontent.com/zakaria220/TvWatch/master/changelog.txt'
            oRequest =  urllib2.Request(sUrl + sRequest)
            oResponse = urllib2.urlopen(oRequest)
            sContent = oResponse.read()
            if "Current Version" in sContent:
                sContent = sContent[sContent.find("Current Version"):]
                if " - " in sContent:
                    sContent = sContent[:sContent.find(" - ")]
                    sContent = sContent.replace("Current Version","")
                    sContent = sContent.replace(" ","")
                    sContent = sContent.replace(".","")
                    newVersion = int(sContent)
                    currentVersion = int(version.replace(".",""))
                    VSlog("checkupdate New Version: " + str(newVersion))
                    VSlog("checkupdate Current Version: " + str(currentVersion))
                    if newVersion > currentVersion:
                        self.oConfig.setSetting('home_update', str('true'))
                        self.oConfig.setSetting('service_time', str(datetime.datetime.now()))
                        dialog = self.oConfig.showInfo("TvWatch", "Mise à jour disponible")
                        return True
                    else:
                        #self.oConfig.showInfo('TvWatch', 'Fichier a jour')
                        self.oConfig.setSetting('service_time', str(datetime.datetime.now()))
                        self.oConfig.setSetting('home_update', str('false'))
        except Exception, e:
            self.oConfig.error(self.oConfig.getlanguage(30205))
            VSlog("checkupdate ERROR: " + e.message)
        return False

    def checkHash(self):
        try:    import json
        except: import simplejson as json

        try:
            sRequest = '?client_id=' + self.client_id + '&client_secret=' + self.client_secret
            sUrl = 'https://api.github.com/repos/zakaria220/TvWatch/contents/addons.xml.md5'
            oRequestHandler = cRequestHandler(sUrl + sRequest)
            sHtmlContent = oRequestHandler.request()
            md5 = json.loads(sHtmlContent)
        except:
            return False

        result = self.resultGit()
        for i in result:
                rootpath = self.getRootPath(i['path'])
                if self.checksize(rootpath, i['size']):
                    VSlog('checkHash')

        return result == 'True'

    def checkdownload(self):
        result = self.resultGit()
        total = len(result)
        dialog = self.oConfig.createDialog('Update')
        site = []
        sdown = 0

        if result:
            for i in result:
                self.oConfig.updateDialog(dialog, total)
                rootpath = self.getRootPath(i['path'])
                if i['type'] == "file":
                    if self.checksize(rootpath, i['size']):
                        try:
                            self.__download(i['download_url'], rootpath)
                            site.append("[COLOR khaki]"+i['name'].encode("utf-8")+"[/COLOR]")
                            sdown = sdown+1
                        except:
                            site.append("[COLOR red]"+i['name'].encode("utf-8")+"[/COLOR]")
                            sdown = sdown+1
                            pass

            self.oConfig.finishDialog(dialog)
            sContent = "Fichier mise à jour %s / %s \n %s" %  (sdown, total, site)
            #self.TextBoxes('TvWatch mise à Jour', sContent)

            self.oConfig.setSetting('service_time', str(datetime.datetime.now()))
            self.oConfig.setSetting('home_update', str('false'))

            fin = self.oConfig.createDialogOK(sContent)
            self.oConfig.update()
        return

    def __download(self, WebUrl, RootUrl):
        inf = urllib.urlopen(WebUrl)
        f = xbmcvfs.File(RootUrl, 'w')
        #save it
        line = inf.read()
        f.write(line)
        inf.close()
        f.close()

    def TextBoxes(self, heading, anounce):
        class TextBox():
            # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()

            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                    f = open(anounce)
                    text = f.read()
                except: text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()
