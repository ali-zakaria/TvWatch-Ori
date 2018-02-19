#-*- coding: utf-8 -*-
# Primatech.
# https://github.com/Kodi-TvWatch/primatech-xbmc-addons
#
from resources . lib . config import cConfig
from resources . lib . util import VSlang , uc , VSlog
from resources . lib . mySqlDB import cMySqlDB
from resources . lib . db import cDb
from resources . lib . gui . gui import cGui

import hashlib , uuid
import xbmc
import base64

if 64 - 64: i11iIiiIii
class OO0o :
 if 81 - 81: Iii1I1 + OO0O0O % iiiii % ii1I - ooO0OO000o
 def __init__ ( self ) :
  self . cC = '0'
  self . cED = uc ( 'MDEvMDEvMTk3MA==' )
  self . cIP = ''
  self . n = ""
  self . p = ""
  self . aD = ""
  self . pU = False
  self . oConfig = cConfig ( )
  if 4 - 4: IiII1IiiIiI1 / iIiiiI1IiI1I1
 def cC0OO ( self ) :
  VSlog ( 'cC0OO checks' )
  o0OoOoOO00 = 0
  self . cC = self . oConfig . getSetting ( uc ( 'dHZXYXRjaENvZGU=' ) )
  I11i = False
  while not self . iCV ( ) :
   VSlog ( "cC: " + self . cC )
   self . cC = self . oConfig . createDialogNum ( VSlang ( int(uc ( 'MzA0MjE=' )) ) )
   I11i = True
   o0OoOoOO00 += 1
   if self . cC == '' or o0OoOoOO00 >= 3 :
    return False
  if self . pU :
   return True
  if self . iEDV ( ) and self . iANIU ( ) :
   if I11i :
    cGui ( ) . showInfo ( VSlang ( int(uc ( 'MzAzMDY=' )) ) % self . p , VSlang ( int(uc ( 'MzA0NDI=' )) ) % self . aD , 7 )
   return True
  else :
   return False
   if 64 - 64: OOooo000oo0 . i1 * ii1IiI1i % IIIiiIIii
 def iCV ( self ) :
  I11iIi1I = cMySqlDB ( ) . getContent ( )
  for IiiIII111iI in I11iIi1I :
   IiII , iI1Ii11111iIi = IiiIII111iI [ 3 ] . split ( "$" )
   if hashlib . sha1 ( self . cC + IiII ) . hexdigest ( ) == iI1Ii11111iIi :
    self . oConfig . setSetting ( uc ( 'dHZXYXRjaENvZGU=' ) , self . cC )
    cDb ( ) . insert_clientID ( str ( IiiIII111iI [ 0 ] ) )
    self . p = IiiIII111iI [ 1 ]
    self . n = IiiIII111iI [ 2 ]
    self . cED = IiiIII111iI [ 4 ]
    self . cIP = IiiIII111iI [ 5 ]
    if 41 - 41: I1II1
    return True
  if I11iIi1I == [ ] :
   self . pU = True
   VSlog ( 'iCV ERROR' )
   VSlog ( 'prolem but TEMCPLV' )
   return True
  VSlog ( 'iCV NOK !' )
  return False
  if 100 - 100: iII1iII1i1iiI % iiIIIII1i1iI % iiI11iii111 % i1I1Ii1iI1ii
 def iEDV ( self ) :
  from datetime import date
  II1iI , i1iIii1Ii1II , i1I1Iiii1111 = self . cED . replace ( " " , "" ) . split ( "/" )
  i11 = date ( int ( i1I1Iiii1111 ) , int ( i1iIii1Ii1II ) , int ( II1iI ) )
  I11 = self . oConfig . getCurrentDate ( )
  if i11 < I11 :
   VSlog ( 'iEDV NOK !' )
   cGui ( ) . showInfo ( uc ( 'QXV0aGVudGlmaWNhdGlvbg==' ) , VSlang ( int(uc ( 'MzA0NTA=' )) ) , 3 )
   return False
  else :
   if 98 - 98: I1111 * o0o0Oo0oooo0 / I1I1i1 * I1I1i1 / ooO0OO000o
   self . aD = str ( ( i11 - I11 ) . days )
   self . oConfig . setSetting ( uc ( 'ZXhwaXJhdGlvbkRhdGU=' ) , self . aD )
   return True
   if 11 - 11: IiII1IiiIiI1 % ii1IiI1i - iIiiiI1IiI1I1
 def iANIU ( self ) :
  oo0O000OoO = True
  i1iiIIiiI111 = self . oConfig . getSetting ( uc ( 'aXNQbGF5aW5n' ) )
  i1iiIIiiIlll = self . oConfig . getSetting ( uc ( 'bXlTZWxmUGxheQ==' ) )
  if i1iiIIiiI111 == '' :
   self . oConfig . setSetting ( uc ( 'aXNQbGF5aW5n' ) , self . cIP )
  else :
   if int ( self . cIP ) > int ( i1iiIIiiI111 ) and i1iiIIiiIlll != 'True' :
    self . oConfig . setSetting ( uc ( 'aXNQbGF5aW5n' ) , self . cIP )
    VSlog ( 'iANIU NOK !' )
    cGui ( ) . showInfo ( uc ( 'QXV0aGVudGlmaWNhdGlvbg==' ) , VSlang ( int(uc ( 'MzA0Mzc=' )) ) , 3 )
    oo0O000OoO = False
  return oo0O000OoO
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
