#-*- coding: utf-8 -*-

import mysql.connector

SITE_IDENTIFIER = 'cMySqlDB'
SITE_NAME = 'MySqlDB'

class cMySqlDB:

    def __init__(self):
        try:
            self.db = mysql.connector.connect(host="sql11.freemysqlhosting.net", \
                                              user="sql11217561", \
                                              password="Wdfqrjffkk", \
                                              database="sql11217561", \
                                              connection_timeout=10)
            self.dbcur = self.db.cursor()
            # self.deleteTable()
            # self.log("Init cMySqlDB SUCCESS")
        except:
            self.log("Init cMySqlDB FAIL")

    def __del__(self):
        try:
            self.dbcur.close()
            self.db.close()
            # self.log("Destroy cMySqlDB SUCCESS")
        except:
            self.log("Destroy cMySqlDB FAIL")

    def createTable(self):
        sql_create = """CREATE TABLE IF NOT EXISTS mainTable (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    prenom VARCHAR(50) NOT NULL,
                    nom VARCHAR(50) NOT NULL,
                    code VARCHAR(73) NOT NULL UNIQUE,
                    expDate VARCHAR(10) NOT NULL,
                    isPlaying VARCHAR(5) NOT NULL
                    );"""
        try:
            self.dbcur.execute(sql_create)
            self.log('Table mainTable MySQL initialized')
        except Exception, e:
            self.log('MySQL ERROR _create_tables mainTable: ' + e.message)

    #***********************************
    #   history fonctions
    #***********************************

    def insertContent(self, meta):
        try:
            ex = """INSERT INTO mainTable (prenom, nom, code, expDate, isPlaying)
                    VALUES(%(prenom)s, %(nom)s, %(code)s, %(expDate)s, %(isPlaying)s)"""
            self.dbcur.execute(ex, meta)
            self.db.commit()
            self.log('SQL INSERT table Successfully')
        except Exception, e:
            self.log('SQL ERROR INSERT table: ' + e.message)

    def updateContent(self, meta, code):
        if meta['prenom']:
            try:
                ex = """UPDATE mainTable
                        SET prenom = %s
                        WHERE code = %s"""
                self.dbcur.execute(ex, (meta['prenom'], code))
                self.db.commit()
                self.log('SQL UPDATE table Successfully: prenom')
            except Exception, e:
                self.log('SQL ERROR UPDATE table prenom: ' + e.message)

        if meta['nom']:
            try:
                ex = """UPDATE mainTable
                        SET nom = %s
                        WHERE code = %s"""
                self.dbcur.execute(ex, (meta['nom'], code))
                self.db.commit()
                self.log('SQL UPDATE table Successfully: nom')
            except Exception, e:
                self.log('SQL ERROR UPDATE table nom: ' + e.message)

        if meta['code']:
            try:
                ex = """UPDATE mainTable
                        SET code = %s
                        WHERE code = %s"""
                self.dbcur.execute(ex, (meta['code'], code))
                self.db.commit()
                self.log('SQL UPDATE table Successfully: code')
            except Exception, e:
                self.log('SQL ERROR UPDATE table code: ' + e.message)

        if meta['expDate']:
            try:
                ex = """UPDATE mainTable
                        SET expDate = %s
                        WHERE code = %s"""
                self.dbcur.execute(ex, (meta['expDate'], code))
                self.db.commit()
                self.log('SQL UPDATE table Successfully: expDate')
            except Exception, e:
                self.log('SQL ERROR UPDATE table expDate: ' + e.message)

        if meta['isPlaying']:
            try:
                ex = """UPDATE mainTable
                        SET isPlaying = %s
                        WHERE code = %s"""
                self.dbcur.execute(ex, (meta['isPlaying'], code))
                self.db.commit()
                self.log('SQL UPDATE table Successfully: isPlaying with ' + meta['isPlaying'])
            except Exception, e:
                self.log('SQL ERROR UPDATE table isPlaying: ' + e.message)

    def updateIsPlaying(self, isPlaying, clientID):
        if isPlaying:
            try:
                ex = """UPDATE mainTable
                        SET isPlaying = %s
                        WHERE id = %s"""
                self.dbcur.execute(ex, (isPlaying, clientID))
                self.db.commit()
                self.log('SQL UPDATE table Successfully: isPlaying with ' + isPlaying)
            except Exception, e:
                self.log('SQL ERROR UPDATE table isPlaying: ' + e.message)

    def getContent(self):
        sql_select = "SELECT * FROM mainTable"
        res = []
        try:
            self.dbcur.execute(sql_select)
            res = self.dbcur.fetchall()
        except Exception, e:
            self.log('SQL ERROR GET table: ' + e.message)
        return res

    def getRegisteredCodes(self):
        sql_select = "SELECT code FROM mainTable"
        res = []
        try:
            self.dbcur.execute(sql_select)
            res = self.dbcur.fetchall()
        except Exception, e:
            self.log('SQL ERROR GET table: ' + e.message)
        return res

    def getContentByCode(self, code):
        sql_select = "SELECT * FROM mainTable WHERE code = '%s'" % (code)
        res = []
        try:
            self.dbcur.execute(sql_select)
            res = self.dbcur.fetchall()
        except Exception, e:
            self.log('SQL ERROR GET table: ' + e.message)
        return res

    def delContent(self, code = None, deleteAll = False):
        res = False
        if code:
            sql_delete = "DELETE FROM mainTable WHERE code = '%s'" % (code)
            try:
                self.dbcur.execute(sql_delete)
                self.db.commit()
                self.log('delContent: successfully')
                res = True
            except Exception, e:
                self.log('SQL ERROR DELETE table: ' + e.message)
                res = False

        if deleteAll:
            sql_delete = "DELETE FROM mainTable"
            try:
                self.dbcur.execute(sql_delete)
                self.db.commit()
                self.log('delContent: successfully')
                res = res and True
            except Exception, e:
                self.log('SQL ERROR DELETE table: ' + e.message)
                res = False
        return res

    def printTables(self):
        sql_delete = "SHOW TABLES"
        try:
            self.dbcur.execute(sql_delete)
            self.log(self.dbcur.fetchall())
        except Exception, e:
            self.log('SQL ERROR printTables : ' + e.message)

    def deleteTable(self):
        try:
            self.dbcur.execute("DROP TABLE IF EXISTS %s" %('mainTable'))
            self.log("deleteTable SUCCESS")
        except:
            self.log("deleteTable FAIL")

    def log(self, output):
        usePrint = True
        try:
            from resources.lib.config import cConfig
            usePrint = False
        except:
            usePrint = True
            pass

        if usePrint:
            print(output)
        else:
            cConfig().log(output)
