# MIT License
#
# Copyright (c) 2020 Arkadiusz Netczuk <dev.arnet@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


import logging

from . import uiloader
from . import resources
from .qt import qApp, QtCore, QEvent


_LOGGER = logging.getLogger(__name__)


UiTargetClass, QtBaseClass = uiloader.loadUiFromClassName( __file__ )


class MainWindow(QtBaseClass):

    logger = None

    def __init__(self):
        super().__init__()

        self.ui = UiTargetClass()
        self.ui.setupUi(self)

        self.settingsFilePath = None

#         self.ui.textEdit.installEventFilter( self )

#         self.statusBar().showMessage("Ready")


    def loadSettings(self):
        settings = self.getSettings()
        self.logger.debug( "loading app state from %s", settings.fileName() )
#         self.ui.appSettings.loadSettings( settings )

        ## restore widget state and geometry
        settings.beginGroup( self.objectName() )
        geometry = settings.value("geometry")
        state = settings.value("windowState")
        if geometry is not None:
            self.restoreGeometry( geometry )
        if state is not None:
            self.restoreState( state )
        settings.endGroup()

#         ## store geometry of all widgets
#         widgets = self.findChildren(QWidget)
#         for w in widgets:
#             wKey = getWidgetKey(w)
#             settings.beginGroup( wKey )
#             geometry = settings.value("geometry")
#             if geometry is not None:
#                 w.restoreGeometry( geometry );
#             settings.endGroup()

    def saveSettings(self):
        settings = self.getSettings()
        self.logger.debug( "saving app state to %s", settings.fileName() )
#         self.ui.appSettings.saveSettings( settings )

        ## store widget state and geometry
        settings.beginGroup( self.objectName() )
        settings.setValue("geometry", self.saveGeometry() )
        settings.setValue("windowState", self.saveState() )
        settings.endGroup()

#         ## store geometry of all widgets
#         widgets = self.findChildren(QWidget)
#         for w in widgets:
#             wKey = getWidgetKey(w)
#             settings.beginGroup( wKey )
#             settings.setValue("geometry", w.saveGeometry() );
#             settings.endGroup()

        ## force save to file
        settings.sync()

    def getSettings(self):
#         ## store in app directory
#         if self.settingsFilePath is None:
# #             scriptDir = os.path.dirname(os.path.realpath(__file__))
# #             self.settingsFilePath = os.path.realpath( scriptDir + "../../../../tmp/settings.ini" )
#             self.settingsFilePath = "settings.ini"
#         settings = QtCore.QSettings(self.settingsFilePath, QtCore.QSettings.IniFormat, self)

        ## store in home directory
        orgName = qApp.organizationName()
        appName = qApp.applicationName()
        settings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, orgName, appName, self)
        return settings


    ## ========================================================================

    
    def eventFilter( self, obj, event ):
        ### context menu disabled in Ui file (Qt Designer)
#         if obj is self.ui.textEdit:
#             if event.type() == QEvent.ContextMenu:
#                 _LOGGER.info( "event intercepted: %s %s", obj, event )
#                 return True
        return super(MainWindow, self).eventFilter( obj, event )


MainWindow.logger = _LOGGER.getChild(MainWindow.__name__)


def getWidgetKey(widget):
    if widget is None:
        return None
    retKey = widget.objectName()
    widget = widget.parent()
    while widget is not None:
        retKey = widget.objectName() + "-" + retKey
        widget = widget.parent()
    return retKey
