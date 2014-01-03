# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008 SISTHEO eric@vernichon.fr  All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
import uno
import xmlrpclib

# a UNO struct later needed to create a document
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK
from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from com.sun.star.awt import Size
from com.sun.star.lang import XMain
from com.sun.star.awt import Rectangle
from com.sun.star.awt import WindowDescriptor
from  com.sun.star.awt.PushButtonType import CANCEL as BUTTON_CANCEL
import unohelper
from com.sun.star.awt.WindowClass import MODALTOP
from com.sun.star.awt.VclWindowPeerAttribute import OK, OK_CANCEL, YES_NO, YES_NO_CANCEL, RETRY_CANCEL, DEF_OK, DEF_CANCEL, DEF_RETRY, DEF_YES, DEF_NO
from com.sun.star.awt import XActionListener
from com.sun.star.awt import XMouseListener
from com.sun.star.awt import XKeyListener

class Sortie( unohelper.Base, XActionListener ):
    def __init__(self, dialog):
        self.dialog = dialog
    def actionPerformed(self, actionEvent):
        dialog.dispose()

class Importation( unohelper.Base, XActionListener ):
    def __init__(self, serveur,user,mdp,objet,port,base,colonnes):
        self.nCount = 0
        self.serveur=serveur
        self.user=user
        self.mdp=mdp
        self.objet=objet
        self.port=port
        self.base=base
        self.colonnes=colonnes

    def actionPerformed(self, actionEvent):
        try:
            cree_importation(self.serveur.Text,self.user.Text,self.mdp.Text,self.objet.getSelectedItem(),self.port.Text,self.base.getSelectedItem(),self.colonnes.SelectedItems,self)
        except Exception,e:
            TestMessageBox(str(e),"Erreur Bouton Import")

class RefreshObjetListener( unohelper.Base, XActionListener ):
    def __init__(self, serveur,user,mdp,objet,port,base,liste):
        self.nCount = 0
        self.serveur=serveur
        self.user=user
        self.mdp=mdp
        self.objet=objet
        self.port=port
        self.base=base
        self.liste=liste

    def actionPerformed(self, actionEvent):
        compteur_objet = 0
        try:
            self.liste.removeItems(0,self.liste.getItemCount())
            for objet in liste_objets(self.serveur.Text,self.user.Text,self.mdp.Text,self.port.Text,self.base.getSelectedItem()):
                compteur_objet=compteur_objet+1
                self.liste.addItem(str(objet),compteur_objet)
        except Exception,e:
            TestMessageBox(str(e),"Erreur Bouton Refresh Objet")

class RefreshMouseObjetListener( unohelper.Base, XMouseListener ):
    def __init__(self, serveur,user,mdp,objet,port,base,liste):
        print "Mouse LIstener"
        self.nCount = 0
        self.serveur=serveur
        self.user=user
        self.mdp=mdp
        self.objet=objet
        self.port=port
        self.base=base
        self.liste=liste

    def mousePressed(self, mouseEvent):
        print "Mouse event ",mouseEvent
        compteur_objet = 0
        try:
            self.liste.removeItems(0,self.liste.getItemCount())
            for objet in liste_objets(self.serveur.Text,self.user.Text,self.mdp.Text,self.port.Text,self.base.getSelectedItem()):
                compteur_objet=compteur_objet+1
                self.liste.addItem(str(objet),compteur_objet)
        except Exception,e:
            TestMessageBox(str(e),"Erreur Bouton Refresh Objet")


class RefreshMouseColonnesListener( unohelper.Base, XMouseListener ):
    def __init__(self, serveur,user,mdp,port,objet,base,liste):
        self.nCount = 0
        self.liste=liste
        self.base=base
        self.objet=objet
        self.mdp=mdp
        self.serveur=serveur
        self.user=user
        self.port=port


    def mousePressed(self, mouseEvent):
        compteur_colonne=0
        print "Action refresh Colonnes"
        #,self.serveur.Text,self.user.Text,self.mdp.Text,self.port.Text,self.base.getSelectedItem(),self.objet.getSelectedItem()
        #print self.serveur.Text,self.user.Text,self.mdp.Text,self.port.Text,self.base.getSelectedItem(),self.objet.getSelectedItem()
        #print liste
        try:
            self.liste.removeItems(0,self.liste.getItemCount())
            #def liste_colonnes(serveurip,user,pwd,port,base,objet):
            print self.serveur.Text,self.user.Text,self.mdp.Text,self.port.Text,self.base.getSelectedItem(),self.objet.getSelectedItem()
            liste_de_colonnes =liste_colonnes(self.serveur.Text,self.user.Text,self.mdp.Text,self.port.Text,self.base.getSelectedItem(),self.objet.getSelectedItem())
            print "liste de colonne ", liste_de_colonnes
            for db in liste_de_colonnes:
                compteur_colonne=compteur_colonne+1
                #print str(db)
                self.liste.addItem(str(db),compteur_colonne)
        except Exception,e:
            TestMessageBox(str(e),"Erreur Bouton Refresh Colonne")

class RefreshKeyColonnesListener( unohelper.Base, XKeyListener ):
    def __init__(self, serveur,user,mdp,port,objet,base,liste):
        self.nCount = 0
        self.liste=liste
        self.base=base
        self.objet=objet
        self.mdp=mdp
        self.serveur=serveur
        self.user=user
        self.port=port


    def keyPressed(self, keyEvent):
        compteur_colonne=0
        try:
            self.liste.removeItems(0,self.liste.getItemCount())
            liste_de_colonnes =liste_colonnes(self.serveur.Text,self.user.Text,self.mdp.Text,self.port.Text,self.base.getSelectedItem(),self.objet.getSelectedItem())
            for db in liste_de_colonnes:
                compteur_colonne=compteur_colonne+1
                self.liste.addItem(str(db),compteur_colonne)
        except Exception,e:
            TestMessageBox(str(e),"Erreur Bouton Refresh Colonne")

class RefreshColonnesListener( unohelper.Base, XActionListener ):
    def __init__(self, serveur,user,mdp,port,objet,base,liste):
        self.nCount = 0
        self.liste=liste
        self.base=base
        self.objet=objet
        self.mdp=mdp
        self.serveur=serveur
        self.user=user
        self.port=port


    def actionPerformed(self, actionEvent):
        compteur_colonne=0
        print "Action refresh Colonnes"
        #,self.serveur.Text,self.user.Text,self.mdp.Text,self.port.Text,self.base.getSelectedItem(),self.objet.getSelectedItem()
        #print self.serveur.Text,self.user.Text,self.mdp.Text,self.port.Text,self.base.getSelectedItem(),self.objet.getSelectedItem()
        #print liste
        try:
            self.liste.removeItems(0,self.liste.getItemCount())
            #def liste_colonnes(serveurip,user,pwd,port,base,objet):
            print self.serveur.Text,self.user.Text,self.mdp.Text,self.port.Text,self.base.getSelectedItem(),self.objet.getSelectedItem()
            liste_de_colonnes =liste_colonnes(self.serveur.Text,self.user.Text,self.mdp.Text,self.port.Text,self.base.getSelectedItem(),self.objet.getSelectedItem())
            print "liste de colonne ", liste_de_colonnes
            for db in liste_de_colonnes:
                compteur_colonne=compteur_colonne+1
                #print str(db)
                self.liste.addItem(str(db),compteur_colonne)
        except Exception,e:
            TestMessageBox(str(e),"Erreur Bouton Refresh Colonne")

class RefreshDbListener( unohelper.Base, XActionListener ):
    def __init__(self, serveur,port,liste):
        self.nCount = 0
        self.liste=liste
        self.serveur=serveur
        self.port=port


    def actionPerformed(self, actionEvent):
        compteur_base = 0
        try:
            self.liste.removeItems(0,self.liste.getItemCount())
            for db in liste_bases(self.serveur.Text,self.port.Text):
                compteur_base=compteur_base+1
                self.liste.addItem(str(db),compteur_base)
        except Exception,e:
            TestMessageBox(str(e),"Erreur Bouton Refresh DB")


def createDialog():

    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager

    # create the dialog model and set the properties
    dialogModel = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialogModel", ctx)
    dialogModel.PositionX = 40
    dialogModel.PositionY = 20
    dialogModel.Width = 250
    dialogModel.Height = 350
    dialogModel.Title = "Configuration"
    dialogModel.Closeable = True
    dialogModel.Sizeable = True

    # Champ de saisie pour le serveur
    labelServeur = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel" )
    labelServeur.PositionX = 10
    labelServeur.PositionY = 20
    labelServeur.Width  = 70
    labelServeur.Height = 14
    labelServeur.Name = "labelServeur"
    labelServeur.Label = "Serveur"

    serveurSaisie = dialogModel.createInstance("com.sun.star.awt.UnoControlEditModel" )
    serveurSaisie.PositionX = 50
    serveurSaisie.PositionY = 20
    serveurSaisie.Width  = 70
    serveurSaisie.Height = 14
    serveurSaisie.Name = "serveur"
    serveurSaisie.TabIndex = 1
    serveurSaisie.Text = "127.0.0.1"

    labelPort = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel" )
    labelPort.PositionX = 10
    labelPort.PositionY = 40
    labelPort.Width  = 70
    labelPort.Height = 14
    labelPort.Name = "labelPort"
    labelPort.Label = "Port"

    portSaisie = dialogModel.createInstance("com.sun.star.awt.UnoControlEditModel" )
    portSaisie.PositionX = 50
    portSaisie.PositionY = 40
    portSaisie.Width  = 70
    portSaisie.Height = 14
    portSaisie.Name = "Port"
    portSaisie.TabIndex = 2
    portSaisie.Text = "8069"

    labelUser = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel" )
    labelUser.PositionX = 10
    labelUser.PositionY = 60
    labelUser.Width  = 70
    labelUser.Height = 14
    labelUser.Name = "labelUser"
    labelUser.Label = "User"


    userSaisie = dialogModel.createInstance("com.sun.star.awt.UnoControlEditModel" )
    userSaisie.PositionX = 50
    userSaisie.PositionY = 60
    userSaisie.Width  = 70
    userSaisie.Height = 14
    userSaisie.Name = "user"
    userSaisie.TabIndex = 3
    userSaisie.Text = "admin"

    labelMdp = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel" )
    labelMdp.PositionX = 10
    labelMdp.PositionY = 80
    labelMdp.Width  = 70
    labelMdp.Height = 14
    labelMdp.Name = "labelMdp"
    labelMdp.Label = "Mot de Passe"

    mdpSaisie = dialogModel.createInstance("com.sun.star.awt.UnoControlEditModel" )
    mdpSaisie.PositionX = 50
    mdpSaisie.PositionY = 80
    mdpSaisie.Width  = 70
    mdpSaisie.Height = 14
    mdpSaisie.Name = "mdp"
    mdpSaisie.TabIndex = 4
    mdpSaisie.Text = "admin"


    labelObj = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel" )
    labelObj.PositionX = 10
    labelObj.PositionY = 100
    labelObj.Width  = 70
    labelObj.Height = 14
    labelObj.Name = "labelObj"
    labelObj.Label = "Objet"


    objSaisie = dialogModel.createInstance("com.sun.star.awt.UnoControlListBoxModel" )
    objSaisie.PositionX = 50
    objSaisie.PositionY = 100
    objSaisie.Width  = 130
    objSaisie.Height = 140
    objSaisie.Name = "objet"
    objSaisie.TabIndex = 7



    labelDb = dialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel" )
    labelDb.PositionX = 150
    labelDb.PositionY = 10
    labelDb.Width  = 70
    labelDb.Height = 14
    labelDb.Name = "labelDb"
    labelDb.Label = "Bases"

    dbSaisie = dialogModel.createInstance("com.sun.star.awt.UnoControlListBoxModel" )
    dbSaisie.PositionX = 150
    dbSaisie.PositionY = 20
    dbSaisie.Width  = 70
    dbSaisie.Height = 50
    dbSaisie.Name = "base"
    dbSaisie.TabIndex = 6

    listecolonnes = dialogModel.createInstance("com.sun.star.awt.UnoControlListBoxModel" )
    listecolonnes.PositionX = 50
    listecolonnes.PositionY = 250
    listecolonnes.Width  = 130
    listecolonnes.Height = 70
    listecolonnes.Name = "colonnes"
    listecolonnes.MultiSelection = 1
    listecolonnes.Dropdown = 0
    listecolonnes.TabIndex = 1

    buttonRefreshObjet = dialogModel.createInstance(
        "com.sun.star.awt.UnoControlButtonModel" )
    buttonRefreshObjet.PositionX = 190
    buttonRefreshObjet.PositionY  = 110
    buttonRefreshObjet.Width = 50
    buttonRefreshObjet.Height = 15
    buttonRefreshObjet.Name = "buttonRefreshObjet"
    buttonRefreshObjet.TabIndex = 5
    buttonRefreshObjet.Label = "Rafraichir Objets"

    buttonRefreshDb = dialogModel.createInstance(
        "com.sun.star.awt.UnoControlButtonModel" )
    buttonRefreshDb.PositionX = 190
    buttonRefreshDb.PositionY  = 90
    buttonRefreshDb.Width = 50
    buttonRefreshDb.Height = 15
    buttonRefreshDb.Name = "buttonRefreshDb"
    buttonRefreshDb.TabIndex = 10
    buttonRefreshDb.Label = "Rafraichir Bases"


    buttonModel = dialogModel.createInstance(
        "com.sun.star.awt.UnoControlButtonModel" )
    buttonModel.PositionX = 190
    buttonModel.PositionY  = 150
    buttonModel.Width = 50
    buttonModel.Height = 14
    buttonModel.Name = "buttonImport"
    buttonModel.TabIndex = 11
    buttonModel.Label = "OK"

    buttonColonnes = dialogModel.createInstance(
        "com.sun.star.awt.UnoControlButtonModel" )
    buttonColonnes.PositionX = 190
    buttonColonnes.PositionY  = 130
    buttonColonnes.Width = 50
    buttonColonnes.Height = 14
    buttonColonnes.Name = "buttonColonnes"
    buttonColonnes.TabIndex = 12
    buttonColonnes.Label = "Colonnes"

    buttonCancel = dialogModel.createInstance(
        "com.sun.star.awt.UnoControlButtonModel" )
    buttonCancel.PositionX = 190
    buttonCancel.PositionY  = 210
    buttonCancel.Width = 50
    buttonCancel.Height = 14
    buttonCancel.Name = "buttonCancel"
    buttonCancel.TabIndex = 11
    buttonCancel.Label = "Cancel"

    # insert the control models into the dialog model

    dialogModel.insertByName( "labelServeur", labelServeur)
    dialogModel.insertByName( "labelUser", labelUser)
    dialogModel.insertByName( "labelObj", labelObj)
    dialogModel.insertByName( "labelMdp", labelMdp)
    dialogModel.insertByName( "labelPort", labelPort)
    dialogModel.insertByName( "labelDb", labelDb)
    dialogModel.insertByName( "serveur", serveurSaisie)
    dialogModel.insertByName( "user", userSaisie)
    dialogModel.insertByName( "mdp", mdpSaisie)
    dialogModel.insertByName( "objet", objSaisie)
    dialogModel.insertByName( "base", dbSaisie)
    dialogModel.insertByName( "colonnes", listecolonnes)
    dialogModel.insertByName( "port", portSaisie)
    dialogModel.insertByName( "buttonRefreshDb",buttonRefreshDb)
    dialogModel.insertByName( "buttonImport", buttonModel)
    dialogModel.insertByName( "buttonCancel",buttonCancel)


    # create the dialog control and set the model
    controlContainer = smgr.createInstanceWithContext(
        "com.sun.star.awt.UnoControlDialog", ctx)
    controlContainer.setModel(dialogModel)

    # add the action listener
    controlContainer.getControl("buttonImport").addActionListener(
        Importation( controlContainer.getControl( "serveur" ), controlContainer.getControl( "user" ), controlContainer.getControl( "mdp" ), controlContainer.getControl( "objet" ), controlContainer.getControl( "port" ),controlContainer.getControl( "base" ),controlContainer.getControl( "colonnes" )))

    buttonCancel.PushButtonType = BUTTON_CANCEL


    controlContainer.getControl("buttonRefreshDb").addActionListener(
        RefreshDbListener(controlContainer.getControl( "serveur" ), controlContainer.getControl( "port" ),controlContainer.getControl("base")))

    controlContainer.getControl("base").addMouseListener(
        RefreshMouseObjetListener(controlContainer.getControl( "serveur" ), controlContainer.getControl( "user" ), controlContainer.getControl( "mdp" ), controlContainer.getControl( "objet" ), controlContainer.getControl( "port" ),controlContainer.getControl( "base" ),controlContainer.getControl( "objet" )))

    controlContainer.getControl("objet").addMouseListener(
         RefreshMouseColonnesListener(controlContainer.getControl( "serveur" ), controlContainer.getControl( "user" ), controlContainer.getControl( "mdp" ),  controlContainer.getControl( "port" ),controlContainer.getControl( "objet" ),controlContainer.getControl( "base" ),controlContainer.getControl( "colonnes" )))

    controlContainer.getControl("objet").addKeyListener(
        RefreshKeyColonnesListener(controlContainer.getControl( "serveur" ), controlContainer.getControl( "user" ), controlContainer.getControl( "mdp" ),  controlContainer.getControl( "port" ),controlContainer.getControl( "objet" ),controlContainer.getControl( "base" ),controlContainer.getControl( "colonnes" )))

    toolkit = smgr.createInstanceWithContext(
        "com.sun.star.awt.ExtToolkit", ctx);

    controlContainer.setVisible(False);
    controlContainer.createPeer(toolkit, None);
    # execute it
    controlContainer.execute()

    # dispose the dialog
    controlContainer.dispose()

def ListBox_mousePressed( ev ):
    print "Bouton presse" ,ev
      #~ If ev.Buttons = com.sun.star.awt.MouseButton.LEFT AND _
          #~ ev.ClickCount = 2 Then

        #~ ' ignore if not selected
        #~ If ev.Source.getSelectedItemPos() > -1 Then

          #~ oDialog = ev.Source.getContext()
          #~ btn_OK = oDialog.getControl("btn_OK")
          #~ oAccOK = btn_OK.getAccessibleContext()
          #~ If oAccOK.getAccessibleActionCount() > 0 Then
            #~ oAccOK.doAccessibleAction(0) ' push
          #~ End If
        #~ End If
      #~ End If
    #~ End Sub

def ListBox_mouseReleased( ev ):
    return 0
def ListBox_mouseEntered( ev ):
    return 0
def ListBox_mouseExited( ev ):
    return 0
def ListBox_disposing( ev ):
    return 0

def TestMessageBox(texte,titre=""):
    try:
        doc = XSCRIPTCONTEXT.getDocument()
        parentwin = doc.CurrentController.Frame.ContainerWindow
        s = texte
        res = MessageBox(parentwin, s, titre, "errorbox", OK)
    except Exception,e:
        print str(e)

def OKMessageBox(texte,titre=""):
    try:
        doc = XSCRIPTCONTEXT.getDocument()
        parentwin = doc.CurrentController.Frame.ContainerWindow
        s = texte
        res = MessageBox(parentwin, s, titre, "infobox", OK)
    except Exception,e:
        print str(e)

def MessageBox( ParentWin,MsgText, MsgTitle, MsgType="messbox", MsgButtons=OK):

    MsgType = MsgType.lower()

    #available msg types
    MsgTypes = ("messbox", "infobox", "errorbox", "warningbox", "querybox")

    if not ( MsgType in MsgTypes ):
        MsgType = "messbox"

    #describe window properties.
    aDescriptor = WindowDescriptor()
    aDescriptor.Type = MODALTOP
    aDescriptor.WindowServiceName = MsgType
    aDescriptor.ParentIndex = -1
    aDescriptor.Parent = ParentWin
    #aDescriptor.Bounds = Rectangle()
    aDescriptor.WindowAttributes = MsgButtons

    tk = ParentWin.getToolkit()
    msgbox = tk.createWindow(aDescriptor)

    msgbox.setMessageText(MsgText)
    if MsgTitle :
        msgbox.setCaptionText(MsgTitle)

    return msgbox.execute()

def liste_bases(serveurip="127.0.0.1",port="8069"):
    url="http://"+serveurip+":"+port+"/xmlrpc/"
    try:
        dbs=xmlrpclib.ServerProxy(url+'db').list()
        dbs.sort()
    except:
        dbs=["Pas de base"]
        return dbs
    return dbs

def liste_objets(serveurip,user,pwd,port,base):
    url="http://"+serveurip+":"+port+"/xmlrpc/"
    server =xmlrpclib.ServerProxy(url+'common')
    sock = xmlrpclib.ServerProxy(url+'object')
    uid= server.login(base,user, pwd)
    ids=sock.execute(base,uid,pwd,'ir.model', 'search', [], 0, 80000)
    liste_objet=[]
    for id in ids :
        champs =sock.execute(base,uid,pwd,'ir.model', 'read', [id])
        liste_objet.append(champs[0]['model'])
    liste_objet.sort()
    return liste_objet

def liste_colonnes(serveurip,user,pwd,port,base,objet):
    if len(objet)>0 :
        print "liste colonne",objet
        url="http://"+serveurip+":"+port+"/xmlrpc/"
        server =xmlrpclib.ServerProxy(url+'common')
        sock = xmlrpclib.ServerProxy(url+'object')
        uid= server.login(base,user, pwd)
        struct=sock.execute(base,uid,pwd,objet, 'fields_get')
        struct=list(struct)
        struct.sort()
        print "Struct = ",struct
        return struct
    else:
         OKMessageBox("Vous devez selectionner un objet")
         return []

    #ids=sock.execute(base,uid, pwd,objet, 'search', [], 0, 1)

def cree_importation(serveurip,user,pwd,objet,port,base,colonnes,listener):
    try:
        print "listener ",dir(listener)
        url="http://"+serveurip+":"+port+"/xmlrpc/"
        server =xmlrpclib.ServerProxy(url+'common')
        sock = xmlrpclib.ServerProxy(url+'object')
        uid= server.login(base,user, pwd)
        ctx = uno.getComponentContext()
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
        classeur = XSCRIPTCONTEXT.getDocument()

        nom_feuille=objet.replace('.','_')
        Feuilles = classeur.Sheets
        print "Colonnes",colonnes
        if not Feuilles.hasByName(nom_feuille):
            Feuilles.insertNewByName(nom_feuille,0)
        Feuille = Feuilles.getByName(nom_feuille)

        ids=sock.execute(base,uid, pwd,objet, 'search', [], 0, 80000)
        lignes=[]
        try:
            lignes =sock.execute(base,uid,pwd,objet, 'read', ids)
            struct=sock.execute(base,uid,pwd,objet, 'fields_get')
        except:
            0
        if len(lignes) >0:
            if len(colonnes) == 0:
                colonnes=lignes[0].keys()
            print "Colonnes =",colonnes
            #~ try:
                #~ colonnes.sort()
            #~ except Exception,e:
                #~ TestMessageBox(str(e))

            #~ print "Colonnes Tries=",colonnes
            x=0
            if lignes <> []:
                for nom_col in  colonnes:
                    cle = None
                    if nom_col <> 'id':
                        cle=str(nom_col).replace('\'','')
                    if cle:
                        if struct[cle].has_key('relation'):
                            obj=struct[cle]['relation'] # object de la relation
                            typere= struct[cle]['type'] # type de la relation
                            Feuille.getCellByPosition(x,0).String =obj
                            Feuille.getCellByPosition(x,1).String = typere
                            Feuille.getCellByPosition(x,2).String = cle
                        else:
                            Feuille.getCellByPosition(x,0).String =""
                            Feuille.getCellByPosition(x,1).String = str(struct[cle]['type'])
                            Feuille.getCellByPosition(x,2).String = cle
                        x=x+1

            y=3
            for ligne in  lignes:
                x=0
                for cle in colonnes:
                    valeur=[]
                    if cle <>'id':
                        if struct[cle].has_key('relation'):
                            if ligne[cle]: # la tableau contient au moins un  élément

                                if struct[cle]['type'] == "many2one":
                                    valeur= ligne[cle][1]
                                elif struct[cle]['type'] == "one2many" or struct[cle]['type'] == "many2many" :
                                    for cel in ligne[cle]:
                                        nom =sock.execute(base,uid,pwd,struct[cle]['relation'] , 'name_get', [cel])[0][1]
                                        valeur.append(unicode(nom))
                                else:
                                    print struct[cle]['type']
                            else:
                                valeur="" # tableau vide
                        else:
                            valeur=ligne[cle]
                        if valeur.__class__.__name__ == 'unicode':
                            Feuille.getCellByPosition(x,y).String = unicode(valeur)
                        elif valeur.__class__.__name__ == 'list': # c'est un tableau
                            for chaine in valeur:
                                print "1 x, y" ,x,y
                                Feuille.getCellByPosition(x,y).String =Feuille.getCellByPosition(x,y).String+" | "+ unicode(chaine)
                        else:
                            print "2 x, y" ,x,y
                            Feuille.getCellByPosition(x,y).String = str(valeur)
                    x=x+1
                y=y+1
                doc = XSCRIPTCONTEXT.getDocument()

            classeur.getCurrentController().setActiveSheet(Feuille) # ren la feuille active
            OKMessageBox("Import ok")

        else:
            OKMessageBox("Table Vide")

    except Exception,e:
        TestMessageBox(str(e))




def importation(recursif="False",base="terp",url="http://127.0.0.1:8069/xmlrpc/",user="admin",pwd="admin"):
    createDialog()



g_exportedScripts = importation,
