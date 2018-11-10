# -*- coding: utf-8 -*-

"""
/***************************************************************************
 GeoHeyToolbox
                                 A QGIS plugin
 GeoHey Toolbox
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-11-09
        copyright            : (C) 2018 by GeoHey
        email                : sshuair@gmail.com
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

__author__ = 'GeoHey'
__date__ = '2019-11-09'
__copyright__ = '(C) 2018 by GeoHey'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingProvider

from .china_offset.wgs2gcj import WGS2GCJ
from .china_offset.gcj2wgs import GCJ2WGS
from .china_offset.gcj2bd import GCJ2BD
from .china_offset.bd2gcj import BD2GCJ
from .china_offset.wgs2bd import WGS2BD
from .china_offset.bd2wgs import BD2WGS

class GeoHeyToolboxProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

        # Load algorithms
        self.alglist = [WGS2GCJ(), GCJ2WGS(),  GCJ2BD(), BD2GCJ(), WGS2BD(), BD2WGS()]

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        for alg in self.alglist:
            self.addAlgorithm( alg )

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'GeoHey'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('GeoHey')

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()

    def icon(self):
        return QIcon(os.path.dirname(__file__) + '/icon.png')