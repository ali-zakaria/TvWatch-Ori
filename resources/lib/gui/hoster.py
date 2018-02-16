#-*- coding: utf-8 -*-
# Primatech.
# https://github.com/Kodi-TvWatch/primatech-xbmc-addons
#
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.player import cPlayer
from resources.lib.db import cDb
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.util import VSlog

class cHosterGui:

    SITE_NAME = 'cHosterGui'

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oHoster, sMediaUrl, sThumbnail, protectedLink, sQual, bGetRedirectUrl = False):
        cConfig().log('showHoster')

        params = ['','','','','','','']

        params[0] = oHoster.getPluginIdentifier()
        params[1] = sMediaUrl
        params[2] = protectedLink
        params[3] = oHoster.getFileName()
        params[4] = oHoster.getDisplayName()
        params[5] = sThumbnail
        params[6] = sQual

        #existe dans le menu krypton 17
        # if not util.isKrypton():
        #     oGui.createContexMenuWatch(oGuiElement, oOutputParameterHandler)

        return self.play(params)

    def checkHoster(self, sHosterUrl):
        cConfig().log('checkHoster')
        #securitee
        if (not sHosterUrl):
            return False

        #Petit nettoyage
        sHosterUrl = sHosterUrl.split('|')[0]

        #Recuperation du host
        try:
            sHostName = sHosterUrl.split('/')[2]
        except:
            sHostName = sHosterUrl

        #L'user a active l'url resolver ?
        if cConfig().getSetting('UserUrlResolver') == 'true':
            import urlresolver
            hmf = urlresolver.HostedMediaFile(url=sHosterUrl)
            if hmf.valid_url():
                tmp = self.getHoster('resolver')
                RH = sHosterUrl.split('/')[2]
                RH = RH.replace('www.','')
                tmp.setRealHost( RH[:3].upper() )
                return tmp

        #Gestion classique
        if ('uptostream' in sHostName):
            return self.getHoster('uptostream')

        #Lien telechargeable a convertir en stream
        if ('uptobox' in sHostName):
            return self.getHoster('uptobox')

        #Si aucun hebergeur connu on teste les liens directs
        if (sHosterUrl[-4:] in '.mp4.avi.flv.m3u8.webm'):
            return self.getHoster('lien_direct')

        return False

    def getHoster(self, sHosterFileName):
        exec "from resources.hosters." + sHosterFileName + " import cHoster"
        return cHoster()

    def play(self, params = ['','','','','','','']):
        # oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        protectedLink = oInputParameterHandler.getValue('protectedLink')
        sFileName = oInputParameterHandler.getValue('sFileName')
        sTitle = oInputParameterHandler.getValue('title')
        sThumbnail = oInputParameterHandler.getValue('sThumbnail')
        sQual = ''

        if params != ['','','','','','','']:
            sHosterIdentifier = params[0]
            sMediaUrl = params[1]
            protectedLink = params[2]
            sFileName = params[3]
            sTitle = params[4]
            sThumbnail = params[5]
            sQual = params[6]

        if not sTitle:
            sTitle = sFileName

        if (False):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        VSlog("Hoster - play " + sMediaUrl)

        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        sHosterName = oHoster.getDisplayName()
        # cConfig().showInfo(sHosterName, 'Resolve')

        try:
            oHoster.setUrl(sMediaUrl)
            aLink = oHoster.getMediaLink()

            if aLink[0]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(self.SITE_NAME)
                oGuiElement.setMediaUrl(aLink[1])
                oGuiElement.setTitle(sTitle)
                oGuiElement.setThumbnail(sThumbnail)
                #oGuiElement.setTitle(oHoster.getFileName())
                oGuiElement.getInfoLabel()

                oPlayer = cPlayer()

                #sous titres ?
                if len(aLink) > 2:
                    oPlayer.AddSubtitles(aLink[2])

                return oPlayer.run(oGuiElement, sFileName, aLink[1], protectedLink, sQual)
            else:
                cConfig().error("Fichier introuvable")
                return False

        except Exception, e:
            cConfig().error("Fichier introuvable")
            cConfig().log('play Hoster Erreur ' + e.message)
            return False

        # oGui.setEndOfDirectory()

    def addToPlaylist(self):
        cConfig().log('addToPlaylist')
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        VSlog("Hoster - play " + sMediaUrl)
        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()

        if (aLink[0] == True):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])
            oGuiElement.setTitle(oHoster.getFileName())

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            oGui.showInfo('Playlist', str(oHoster.getFileName()), 5)
            return

        oGui.setEndOfDirectory()

    def __getRedirectUrl(self, sUrl):
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
