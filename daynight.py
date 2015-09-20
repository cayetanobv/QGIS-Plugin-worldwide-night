# -*- coding: utf-8 -*-
#
#  Author: Cayetano Benavent, 2015.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

from datetime import datetime

from qgis.core import *

# To avoid errors if you run module without X11
import matplotlib
matplotlib.use('Agg')

from mpl_toolkits.basemap import Basemap



class DayNight(object):
    """
    Get day and night geometry and dumps
    to a SHP file

    """

    def __init__(self, filepath, input_date=None):
        """
        filepath: destiny file to store output
        SHP with day-night geometry

        input_date = None is for UTC now date
        For others input date: datetime object must be passed

            datetime(year, month, day, hour, minute)

        """
        self.filepath = filepath
        self.input_date = input_date

    def getDayNight(self):
        """
        Get day and night geometry an dumps
        to a SHP file

        Default projection: Equirectangular (Cylindrical Equidistant)

        Default date to compute: now (UTC)

        """
        if self.input_date == None:
            date = datetime.utcnow()
            map_date = date.strftime("%d %b %Y %H:%M:%S")
        else:
            date = self.input_date
            map_date = date.strftime("%d %b %Y %H:%M:%S")

        mp = Basemap(projection='cyl',lon_0=0, ellps='WGS84', resolution=None)

        contour_set = mp.nightshade(date)

        self.__getGeom(contour_set, map_date)

        return 'Day/Night Map for {} (UTC)'.format(map_date)


    def __getGeom(self, contour_set, map_date):
        """
        Get shapefile with an input geometry

        """

        n_coll = len(contour_set.collections)

        for cs_coll in range(n_coll):
            if len(contour_set.collections[cs_coll].get_paths()) > 0:
                cs_paths = contour_set.collections[cs_coll].get_paths()[0]

                vert = cs_paths.vertices

                lon = vert[:,0]
                lat = vert[:,1]

                if len(lon) > 2:
                    self.__buildGeom(lon, lat, map_date)


    def __buildGeom(self, lon, lat, map_date):
        """
        Build shapefile geometry

        """

        qgs_pt = [QgsPoint(coord[0], coord[1]) for coord in zip(lon,lat)]

        pl_ly = QgsVectorLayer("Polygon", "tmp_layer", "memory")
        lys_crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        pl_ly.setCrs(lys_crs)
        prov = pl_ly.dataProvider()

        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPolygon([qgs_pt]))
        prov.addFeatures([feat])

        pl_ly.updateExtents()

        lyrname= "worldwidenight_{}".format(map_date)

        error = QgsVectorFileWriter.writeAsVectorFormat(pl_ly, self.filepath, lyrname, lys_crs, "ESRI Shapefile")

        if error == QgsVectorFileWriter.NoError:
            return 0
