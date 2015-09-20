# -*- coding: utf-8 -*-
"""
/***************************************************************************
 worldwidenight

 This Plugin get worldwide night geometry and export to a shapefile.
                              -------------------
        begin                : 2015-03-21
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

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import *
from qgis.core import *

# Python SL imports
import os.path
import imp
from datetime import datetime

# Initialize Qt resources from file resources.py
import resources_rc

# Import the code for the dialog
from worldwidenight_dialog import worldwidenightDialog

ErrorWWNight = None

try:
    imp.find_module('matplotlib')

    # Import daynight module
    from .daynight import DayNight

except ImportError, err:
    ErrorWWNight = err


class worldwidenight:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'worldwidenight_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = worldwidenightDialog(parent=self.iface.mainWindow())

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Worldwide night to SHP')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'worldwidenight')
        self.toolbar.setObjectName(u'worldwidenight')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('worldwidenight', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/worldwidenight/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Worldwide night to SHP'),
            callback=self.run,
            parent=self.iface.mainWindow())


        # Connecting actions and functions (signals and slots)
        QObject.connect(self.dlg.outputButton, SIGNAL("clicked()"), self.setDestFolder)
        QObject.connect(self.dlg.computeButton, SIGNAL("clicked()"), self.runComputeWorldWideNight)
        QObject.connect(self.dlg.helpButton, SIGNAL("clicked()"), self.getHelp)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Worldwide night to SHP'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        # show the dialog
        self.dlg.show()


    def checkOTF(self):
        """
        Check if OTF CRS Transformation is enabled
        """
        if not self.iface.mapCanvas().mapRenderer().hasCrsTransformEnabled():
            self.iface.mapCanvas().setCrsTransformEnabled(True)
            otfmsg = "OTF CRS Transformation enabled to properly add new layer (with EPSG:4326)"
            self.iface.messageBar().pushMessage("Info", otfmsg, level=QgsMessageBar.INFO)


    def forcingCRS(self, crs_forced):
        """
        Forcing to use CRS EPSG:4326 to create new layer
        """
        self.oldcrs = self.iface.mapCanvas().mapRenderer().destinationCrs()
        self.iface.mapCanvas().mapRenderer().setDestinationCrs(crs_forced)
        self.stgs = QSettings()
        self.oldstgns = self.stgs.value("/Projections/defaultBehaviour")
        self.stgs.setValue("/Projections/defaultBehaviour", "useProject")


    def crsOldSettings(self):
        """
        Enable old settings again
        """
        self.iface.mapCanvas().mapRenderer().setDestinationCrs(self.oldcrs)
        self.stgs.setValue("/Projections/defaultBehaviour", self.oldstgns)


    def runComputeWorldWideNight(self):
        """
        Run computations...
        """

        dest_folder = self.dlg.getOutputPath()

        self.computeWorldWideNight(dest_folder)


    def computeWorldWideNight(self, dest_folder):
        """
        Compute worldwide night
        """

        if ErrorWWNight:
            errmsg = "{}.\nSee Help for requirements.".format(str(ErrorWWNight))
            QMessageBox.warning(self.iface.mainWindow(),"Module not found", errmsg)
            return

        try:
            self.dlg.progressBar.setValue(0)

            lys_crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)

            self.forcingCRS(lys_crs)

            # input_date = None is for UTC now date
            # For others input date: datetime object must be passed
            #       datetime(year, month, day, hour, minute)

            datetime_qt = self.dlg.getDateTime()
            datetime_py = datetime_qt.toPyDateTime()

            self.dlg.progressBar.setValue(10)

            # Output shp filename
            date_fmt = '%Y%m%d_%H%M%S'
            name = "worldwide_night_{}".format(datetime_py.strftime(date_fmt))
            filename = "{}.shp".format(name)

            # Set output filepath
            filepath = os.path.join(dest_folder, filename)

            if not os.path.exists(dest_folder):
                QMessageBox.information(self.iface.mainWindow(),"Warning", "Set a valid folder path.")
                self.dlg.progressBar.setValue(0)
                return

            dn = DayNight(filepath, input_date=datetime_py)
            dn.getDayNight()

            self.crsOldSettings()

            check_addlayer = self.dlg.getCheckBoxState()

            if check_addlayer:
                self.checkOTF()
                new_lyr = QgsVectorLayer(filepath, name, "ogr")
                new_lyr.setCrs(lys_crs)

                if not new_lyr.isValid():
                    self.iface.messageBar().pushMessage("Error", "Layer failed to load!",
                                                            level=QgsMessageBar.CRITICAL)
                else:
                    QgsMapLayerRegistry.instance().addMapLayer(new_lyr)

            self.dlg.progressBar.setValue(100)

            self.iface.messageBar().pushMessage("Info", "Layer sucessfully created: %s" % (filename),
                                                level=QgsMessageBar.INFO, duration=10)

        except Exception as e:
            result = '{0} - {1}'.format(e.message, e.args)
            self.iface.messageBar().pushMessage("Error", result, level=QgsMessageBar.CRITICAL)
            self.dlg.progressBar.setValue(0)


    def setDestFolder(self):
        """
        Set Destination folder to save shp layer
        """

        self.dlg.progressBar.setValue(0)

        # open file dialog to select folder
        start_dir = '/home'
        folder_path = QFileDialog.getExistingDirectory(self.iface.mainWindow(),
                                                     'Select destination folder to save shp layer',
                                                     start_dir)

        if folder_path:
            self.dlg.setLabelPathOutputFolder(folder_path)
        else:
            self.dlg.setLabelPathOutputFolder("Destination folder...")


    def getHelp(self):
        """
        Show help to users
        """

        QMessageBox.information(self.iface.mainWindow(),"Help",
            """
            1) Select a valid date to compute (UTC).

            2) Select destination folder to
            save output layer (shp)*.

            3) Push button "Compute worldwide night!".

            *Output CRS is EPSG:4326.

            Requirements:
              - Matplotlib Basemap Toolkit Python library:
                 https://github.com/matplotlib/basemap
                 http://matplotlib.org/basemap

            Developed by Cayetano Benavent 2015.

            """)
