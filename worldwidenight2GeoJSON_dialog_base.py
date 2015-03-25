# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'worldwidenight2GeoJSON_dialog_base.ui'
#
# Created: Wed Mar 25 02:03:35 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_worldwidenightDialogBase(object):
    def setupUi(self, worldwidenightDialogBase):
        worldwidenightDialogBase.setObjectName(_fromUtf8("worldwidenightDialogBase"))
        worldwidenightDialogBase.resize(304, 274)
        self.verticalLayout = QtGui.QVBoxLayout(worldwidenightDialogBase)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelDate = QtGui.QLabel(worldwidenightDialogBase)
        self.labelDate.setObjectName(_fromUtf8("labelDate"))
        self.verticalLayout.addWidget(self.labelDate)
        self.dateTimeEdit = QtGui.QDateTimeEdit(worldwidenightDialogBase)
        self.dateTimeEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dateTimeEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2015, 1, 1), QtCore.QTime(12, 0, 0)))
        self.dateTimeEdit.setDate(QtCore.QDate(2015, 1, 1))
        self.dateTimeEdit.setTime(QtCore.QTime(12, 0, 0))
        self.dateTimeEdit.setCurrentSection(QtGui.QDateTimeEdit.YearSection)
        self.dateTimeEdit.setCalendarPopup(True)
        self.dateTimeEdit.setTimeSpec(QtCore.Qt.UTC)
        self.dateTimeEdit.setObjectName(_fromUtf8("dateTimeEdit"))
        self.verticalLayout.addWidget(self.dateTimeEdit)
        self.labelOutput = QtGui.QLabel(worldwidenightDialogBase)
        self.labelOutput.setObjectName(_fromUtf8("labelOutput"))
        self.verticalLayout.addWidget(self.labelOutput)
        self.outputButton = QtGui.QPushButton(worldwidenightDialogBase)
        self.outputButton.setObjectName(_fromUtf8("outputButton"))
        self.verticalLayout.addWidget(self.outputButton)
        self.labelOutputPath = QtGui.QLabel(worldwidenightDialogBase)
        self.labelOutputPath.setFrameShape(QtGui.QFrame.StyledPanel)
        self.labelOutputPath.setObjectName(_fromUtf8("labelOutputPath"))
        self.verticalLayout.addWidget(self.labelOutputPath)
        self.addLayerCheckBox = QtGui.QCheckBox(worldwidenightDialogBase)
        self.addLayerCheckBox.setChecked(True)
        self.addLayerCheckBox.setObjectName(_fromUtf8("addLayerCheckBox"))
        self.verticalLayout.addWidget(self.addLayerCheckBox)
        self.computeButton = QtGui.QPushButton(worldwidenightDialogBase)
        self.computeButton.setObjectName(_fromUtf8("computeButton"))
        self.verticalLayout.addWidget(self.computeButton)
        self.progressBar = QtGui.QProgressBar(worldwidenightDialogBase)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.helpButton = QtGui.QPushButton(worldwidenightDialogBase)
        self.helpButton.setObjectName(_fromUtf8("helpButton"))
        self.verticalLayout.addWidget(self.helpButton)

        self.retranslateUi(worldwidenightDialogBase)
        QtCore.QMetaObject.connectSlotsByName(worldwidenightDialogBase)

    def retranslateUi(self, worldwidenightDialogBase):
        worldwidenightDialogBase.setWindowTitle(_translate("worldwidenightDialogBase", "Worldwide night to GeoJSON", None))
        self.labelDate.setText(_translate("worldwidenightDialogBase", "1) Select date to compute (UTC).", None))
        self.dateTimeEdit.setDisplayFormat(_translate("worldwidenightDialogBase", "yyyy-MM-dd  HH:mm", None))
        self.labelOutput.setText(_translate("worldwidenightDialogBase", "2) Select destination folder for GeoJSON.", None))
        self.outputButton.setText(_translate("worldwidenightDialogBase", "Browse", None))
        self.labelOutputPath.setText(_translate("worldwidenightDialogBase", "Output folder...", None))
        self.addLayerCheckBox.setText(_translate("worldwidenightDialogBase", "Add new layer to map", None))
        self.computeButton.setText(_translate("worldwidenightDialogBase", "Compute worldwide night!", None))
        self.helpButton.setText(_translate("worldwidenightDialogBase", "Help", None))

