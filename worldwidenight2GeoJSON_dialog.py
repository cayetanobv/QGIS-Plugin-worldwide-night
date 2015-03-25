# -*- coding: utf-8 -*-
"""
/***************************************************************************
 worldwidenightDialog
                                 A QGIS plugin
 This Plugin get worldwide night geometry and dumps to a GeoJSON file.
                             -------------------
        begin                : 2015-03-21
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Cayetano Benavent
        email                : cayetano.benavent@geographica.gs
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'worldwidenight2GeoJSON_dialog_base.ui'))


class worldwidenightDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(worldwidenightDialog, self).__init__(parent)
        
        self.setupUi(self)
    
    def getDateTime(self):
        """
        Get date time object from UI
        """
        datetime = self.dateTimeEdit.dateTime()
        
        return datetime
    
    def setLabelPathOutputFolder(self, output):
        self.labelOutputPath.setText(output)
    
    def getOutputPath(self):
        return self.labelOutputPath.text()
    
    def getCheckBoxState(self):
        return self.addLayerCheckBox.isChecked()

