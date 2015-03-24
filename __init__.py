# -*- coding: utf-8 -*-
"""
/***************************************************************************
 worldwidenight
                                 A QGIS plugin
 This Plugin get worldwide night geometry and dumps to a GeoJSON file.
                             -------------------
        begin                : 2015-03-21
        copyright            : (C) 2015 by Cayetano Benavent
        email                : cayetano.benavent@geographica.gs
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load worldwidenight class from file worldwidenight.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .worldwidenight2GeoJSON import worldwidenight
    return worldwidenight(iface)
