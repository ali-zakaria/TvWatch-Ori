#-*- coding: utf-8 -*-

import mysql.connector
from resources.lib.util import VSlog, uc

SITE_IDENTIFIER = 'cMySqlDB'
SITE_NAME = 'MySqlDB'

class cMySqlDB:

    def __init__(self):
        try:
            self.db = mysql.connector.connect(host=uc("c3FsMTEuZnJlZW15c3FsaG9zdGluZy5uZXQ="), \
                                              user=uc("c3FsMTEyMTc1NjE="), \
                                              password=uc("V2RmcXJqZmZraw=="), \
                                              database=uc("c3FsMTEyMTc1NjE="), \
                                              connection_timeout=10)
            self.dbcur = self.db.cursor()
            # VSlog("Init cMySqlDB SUCCESS")
        except:
            VSlog("Init cMySqlDB FAIL")

    def __del__(self):
        try:
            self.dbcur.close()
            self.db.close()
            # VSlog("Destroy cMySqlDB SUCCESS")
        except:
            VSlog("Destroy cMySqlDB FAIL")

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
            VSlog('Table mainTable MySQL initialized')
        except Exception, e:
            VSlog('MySQL ERROR _create_tables mainTable: ' + e.message)

    def updateIP(self, isPlaying, clientID):
        if isPlaying:
            try:
                ex = """UPDATE mainTable
                        SET isPlaying = %s
                        WHERE id = %s"""
                self.dbcur.execute(ex, (isPlaying, clientID))
                self.db.commit()
                VSlog('SQL UPDATE table Successfully: isPlaying with ' + isPlaying)
            except Exception, e:
                VSlog('SQL ERROR UPDATE table isPlaying: ' + e.message)

    def getContent(self):
        sql_select = "SELECT * FROM mainTable"
        res = []
        try:
            self.dbcur.execute(sql_select)
            res = self.dbcur.fetchall()
        except Exception, e:
            VSlog('SQL ERROR GET table: ' + e.message)
        return res
