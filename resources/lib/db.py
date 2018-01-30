#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
import os, sys
import urllib
import xbmc

# import mysql.connector


SITE_IDENTIFIER = 'cDb'
SITE_NAME = 'DB'

try:
    from sqlite3 import dbapi2 as sqlite
    cConfig().log('SQLITE 3 as DB engine')
except:
    from pysqlite2 import dbapi2 as sqlite
    cConfig().log('SQLITE 2 as DB engine')

class cDb:

    def __init__(self):
        DB = cConfig().getFileDB()
        try:
            self.db = sqlite.connect(DB)
            self.dbcur = self.db.cursor()
        except:
            return False

    def __del__(self):
        ''' Cleanup db when object destroyed '''
        try:
            self.dbcur.close()
            self.dbcon.close()
        except: pass

    def _create_tables(self):

        sql_create2 = "DROP TABLE history"

        ''' Create table '''
        sql_create = "CREATE TABLE IF NOT EXISTS history ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""siteurl TEXT, ""title TEXT, ""icon TEXT, ""UNIQUE(siteurl)"");"
        self.dbcur.execute(sql_create)

        sql_create = "CREATE TABLE IF NOT EXISTS resume ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""title TEXT, ""timepoint TEXT, ""UNIQUE(title)"");"
        self.dbcur.execute(sql_create)

        sql_create = "CREATE TABLE IF NOT EXISTS watched ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""title TEXT, ""site TEXT, ""UNIQUE(title, site)"");"
        self.dbcur.execute(sql_create)

        sql_create = "CREATE TABLE IF NOT EXISTS favorite ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""title TEXT, ""siteurl TEXT, ""site TEXT, ""fav TEXT, ""cat TEXT, ""icon TEXT, ""fanart TEXT, ""UNIQUE(title, site)"");"
        self.dbcur.execute(sql_create)

        #sql_create = "DROP TABLE download"
        #self.dbcur.execute(sql_create)

        sql_create = "CREATE TABLE IF NOT EXISTS download ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""title TEXT, ""url TEXT, ""path TEXT, ""cat TEXT, ""icon TEXT, ""size TEXT,""totalsize TEXT, ""status TEXT, ""UNIQUE(title, path)"");"
        self.dbcur.execute(sql_create)

        sql_create = "CREATE TABLE IF NOT EXISTS episodes ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""siteurl TEXT, ""title TEXT, ""icon TEXT, ""UNIQUE(siteurl)"");"
        self.dbcur.execute(sql_create)

        cConfig().log('Table initialized')

    #Ne pas utiliser cette fonction pour les chemins
    def str_conv(self, data):
        if isinstance(data, str):
            # Must be encoded in UTF-8
            data = data.decode('utf8')

        import unicodedata
        data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
        data = data.decode('string-escape') #ATTENTION : provoque des bugs pour les chemins a cause du caractere '/'

        return data

    def str_conv2(self, data):
        data = data.replace(" ", "_")
        data = data.replace("'", "")

        return data

    def insert_resume(self, meta):
        title = self.str_conv2(meta['title'])
        timepoint = meta['timepoint']

        try:
            ex = "INSERT INTO resume (title, timepoint) VALUES (?, ?)"
            self.dbcur.execute(ex, (title, timepoint))
            self.db.commit()
            cConfig().log('SQL INSERT resume Successfully')
            self.db.close()
        except Exception, e:
            cConfig().log('SQL ERROR INSERT resume: ' + e.message)
            pass

    def insert_watched(self, meta):

        title = self.str_conv(meta['title'])
        site = urllib.quote_plus(meta['site'])
        ex = "INSERT INTO watched (title, site) VALUES (?, ?)"
        self.dbcur.execute(ex, (title,site))
        try:
            self.db.commit()
            cConfig().log('SQL INSERT watched Successfully')
        except Exception, e:
            #print ('************* Error attempting to insert into %s cache table: %s ' % (table, e))
            cConfig().log('SQL ERROR INSERT watched: ' + e.message)
            pass
        self.db.close()

    def get_resume(self, meta):
        title = self.str_conv2(meta['title'])

        sql_select = "SELECT * FROM resume WHERE title = '%s'" % (title)
        try:
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            self.dbcur.close()
            return matchedrow
        except Exception, e:
            cConfig().log('SQL ERROR EXECUTE resume: ' + e.message)
            return None

    def get_watched(self, meta):
        count = 0
        site = urllib.quote_plus(meta['site'])
        sql_select = "SELECT * FROM watched WHERE site = '%s'" % (site)

        try:
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            self.dbcur.close()
            if matchedrow:
                count = 1
            return count
        except Exception, e:
            cConfig().log('SQL ERROR EXECUTE watched: ' + e.message)
            return None

    def del_watched(self, meta):
        site = urllib.quote_plus(meta['site'])
        sql_select = "DELETE FROM watched WHERE site = '%s'" % (site)

        try:
            self.dbcur.execute(sql_select)
            self.db.commit()
            self.dbcur.close()
            return False, False
        except Exception, e:
            cConfig().log('SQL ERROR EXECUTE watched: ' + e.message)
            return False, False

    def del_resume(self, title = '', deleteAll = False):

        if title != '':
            sql_delete = "DELETE FROM resume WHERE title = '%s'" % (title)

        if deleteAll:
            sql_delete = "DELETE FROM resume;"

        try:
            self.dbcur.execute(sql_delete)
            self.db.commit()
            self.dbcur.close()
            return
        except Exception, e:
            cConfig().log('SQL ERROR DELETE resume: ' + e.message)
            return

    #***********************************
    #   Favoris fonctions
    #***********************************

    def insert_favorite(self, meta):
        title = self.str_conv(meta['title'])
        siteurl = urllib.quote_plus(meta['siteurl'])
        sIcon = meta['icon']

        try:
            ex = "INSERT INTO favorite (title, siteurl, site, fav, cat, icon, fanart) VALUES (?, ?, ?, ?, ?, ?, ?)"
            self.dbcur.execute(ex, (title,siteurl, meta['site'],meta['fav'],meta['cat'],sIcon,meta['fanart']))
            self.db.commit()
            self.db.close()
            cConfig().log('SQL INSERT favorite Successfully')
            cConfig().showInfo(meta['title'], 'Enregistré avec succés')
        except Exception, e:
            if 'UNIQUE constraint failed' in e.message:
                cConfig().showInfo(meta['title'], 'Item déjà présent dans votre Liste')
            cConfig().log('SQL ERROR INSERT favorite: ' + e.message)
            pass

    def get_favorite(self):
        sql_select = "SELECT * FROM favorite"
        matchedrow = []
        try:
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            self.dbcur.close()
        except Exception, e:
            cConfig().log('SQL ERROR EXECUTE favorite: ' + e.message)
        return matchedrow


    def del_favorite(self):
        oInputParameterHandler = cInputParameterHandler()

        if (oInputParameterHandler.exist('sCat')):
            sql_delete = "DELETE FROM favorite WHERE cat = '%s'" % (oInputParameterHandler.getValue('sCat'))

        if(oInputParameterHandler.exist('sMovieTitle')):
            siteUrl = oInputParameterHandler.getValue('siteUrl')
            sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
            siteUrl = urllib.quote_plus(siteUrl)
            title = self.str_conv(sMovieTitle)
            title = title.replace("'", r"''")
            sql_delete = "DELETE FROM favorite WHERE siteurl = '%s' AND title = '%s'" % (siteUrl,title)

        if(oInputParameterHandler.exist('sAll')):
            sql_delete = "DELETE FROM favorite;"

        try:
            self.dbcur.execute(sql_delete)
            self.db.commit()
            self.dbcur.close()
            cConfig().showInfo('vStream', 'Favoris supprimé')
            cConfig().update()
            return False, False
        except Exception, e:
            cConfig().log('SQL ERROR EXECUTE favorite: ' + e.message)
            return False, False

    def writeFavourites(self):

        oInputParameterHandler = cInputParameterHandler()
        sTitle = oInputParameterHandler.getValue('sTitle')
        sId = oInputParameterHandler.getValue('sId')
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sFav = oInputParameterHandler.getValue('sFav')

        if (oInputParameterHandler.exist('sCat')):
            sCat = oInputParameterHandler.getValue('sCat')
        else:
            sCat = '5'

        sUrl = urllib.quote_plus(sUrl)
        fav_db = self.__sFile
        watched = {}
        if not os.path.exists(fav_db):
            file(fav_db, "w").write("%r" % watched)

        if os.path.exists(fav_db):
            watched = eval(open(fav_db).read() )
            watched[sUrl] = watched.get(sUrl) or []

            #add to watched
            if not watched[sUrl]:
                #list = [sFav, sUrl];
                watched[sUrl].append(sFav)
                watched[sUrl].append(sId)
                watched[sUrl].append(sTitle)
                watched[sUrl].append(sCat)
            else:
                watched[sUrl][0] = sFav
                watched[sUrl][1] = sId
                watched[sUrl][2] = sTitle
                watched[sUrl][3] = sCat

        file(fav_db, "w").write("%r" % watched)
        cConfig().showInfo('Marque-Page', sTitle)
        #fav_db.close()

    #***********************************
    #   Download fonctions
    #***********************************

    def insert_download(self, meta):

        title = self.str_conv(meta['title'])
        url = urllib.quote_plus(meta['url'])
        sIcon = urllib.quote_plus(meta['icon'])
        sPath = meta['path']

        ex = "INSERT INTO download (title, url, path, cat, icon, size, totalsize, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        self.dbcur.execute(ex, (title,url, sPath,meta['cat'],sIcon, '', '', 0))

        try:
            self.db.commit()
            self.db.close()
            cConfig().log('SQL INSERT download Successfully')
            cConfig().showInfo(meta['title'], 'Enregistré avec succés')
        except Exception, e:
            cConfig().log('SQL ERROR INSERT download: ' + e.message)
            pass

    def get_Download(self, meta = ''):
        if meta == '':
            sql_select = "SELECT * FROM download"
        else:
            url = urllib.quote_plus(meta['url'])
            sql_select = "SELECT * FROM download WHERE url = '%s' AND status = '0'" % (url)

        try:
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            self.dbcur.close()
            return matchedrow
        except Exception, e:
            cConfig().log('SQL ERROR EXECUTE download: ' + e.message)
            return None

    def clean_download(self):

        sql_select = "DELETE FROM download WHERE status = '2'"

        try:
            self.dbcur.execute(sql_select)
            self.db.commit()
            self.dbcur.close()
            return False, False
        except Exception, e:
            cConfig().log('SQL ERROR EXECUTE download: ' + e.message)
            return False, False

    def reset_download(self, meta):

        url = urllib.quote_plus(meta['url'])
        sql_select = "UPDATE download SET status = '0' WHERE status = '2' AND url = '%s'" % (url)

        try:
            self.dbcur.execute(sql_select)
            self.db.commit()
            self.dbcur.close()
            return False, False
        except Exception, e:
            cConfig().log('SQL ERROR EXECUTE download: ' + e.message)
            return False, False

    def del_download(self, meta):
        if len(meta['url']) > 1:
            url = urllib.quote_plus(meta['url'])
            sql_select = "DELETE FROM download WHERE url = '%s'" % (url)
        elif len(meta['path']) > 1:
            path = meta['path']
            sql_select = "DELETE FROM download WHERE path = '%s'" % (path)
        else:
            return

        try:
            self.dbcur.execute(sql_select)
            self.db.commit()
            self.dbcur.close()
            return False, False
        except Exception, e:
            cConfig().log('SQL ERROR EXECUTE download: ' + e.message)
            return False, False

    def Cancel_download(self):
        sql_select = "UPDATE download SET status = '0' WHERE status = '1'"
        try:
            self.dbcur.execute(sql_select)
            self.db.commit()
            self.dbcur.close()
            return False, False
        except Exception, e:
            cConfig().log('SQL ERROR EXECUTE download: ' + e.message)
            return False, False

    def update_download(self, meta):

        path = meta['path']
        size = meta['size']
        totalsize = meta['totalsize']
        status = meta['status']

        sql_select = "UPDATE download set size = '%s', totalsize = '%s', status= '%s' WHERE path = '%s'" % (size, totalsize, status, path)

        try:
            self.dbcur.execute(sql_select)
            self.db.commit()
            self.dbcur.close()
            return False, False
        except Exception, e:
            cConfig().log('SQL ERROR EXECUTE download: ' + e.message)
            return False, False

    #***********************************
    #   episodes fonctions
    #***********************************

    def insert_episodes(self, meta):
        title = meta['title']
        siteurl = meta['siteurl']
        sIcon = meta['icon']
        try:
            ex = "INSERT INTO episodes (title, siteurl, icon) VALUES (?, ?, ?)"
            self.dbcur.execute(ex, (title, siteurl, sIcon))
            self.db.commit()
            self.dbcur.close()
            cConfig().log('SQL INSERT Episodes Successfully')
            return True
        except Exception, e:
            cConfig().log('SQL ERROR INSERT episodes: ' + e.message)
            return False

    def get_episodes(self):
        sql_select = "SELECT * FROM episodes"
        try:
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            self.dbcur.close()
            return matchedrow
        except Exception, e:
            cConfig().log('SQL ERROR GET episodes: ' + e.message)
            return None

    def del_episodes(self, siteurl = '', deleteAll = False):
        if siteurl != '':
            sql_delete = "DELETE FROM episodes WHERE siteurl = '%s'" % (siteurl)
        if deleteAll:
            sql_delete = "DELETE FROM episodes;"
        try:
            self.dbcur.execute(sql_delete)
            self.db.commit()
            self.dbcur.close()
            return True
        except Exception, e:
            cConfig().log('SQL ERROR DELETE episodes: ' + e.message)
            return False

    #***********************************
    #   history fonctions
    #***********************************

    def insert_history(self, meta):
        title = meta['title']
        siteurl = meta['siteurl']
        sIcon = meta['icon']
        try:
            ex = "INSERT INTO history (title, siteurl, icon) VALUES (?, ?, ?)"
            self.dbcur.execute(ex, (title, siteurl, sIcon))
            self.db.commit()
            self.db.close()
            cConfig().log('SQL INSERT history Successfully')
            return True
        except Exception, e:
            cConfig().log('SQL ERROR INSERT history: ' + e.message)
            return False


    def get_history(self):
        sql_select = "SELECT * FROM history"
        try:
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            self.dbcur.close()
            return matchedrow
        except Exception, e:
            cConfig().log('SQL ERROR GET history: ' + e.message)
            return None


    def del_history(self, siteurl = '', deleteAll = False):
        if siteurl != '':
            sql_delete = "DELETE FROM history WHERE siteurl = '%s'" % (siteurl)
        if deleteAll:
            sql_delete = "DELETE FROM history;"
        try:
            self.dbcur.execute(sql_delete)
            self.db.commit()
            cConfig().log('del_history: successfully')
            self.dbcur.close()
            return True
        except Exception, e:
            cConfig().log('SQL ERROR DELETE history: ' + e.message)
            return False
