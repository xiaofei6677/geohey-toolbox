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

from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,QgsFeature, QgsGeometry, QgsPointXY, QgsMultiPoint,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink)
from .transform import wgs2gcj

class WGS2GCJ(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(parameters, self.INPUT, context)
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT,
                context, source.fields(), source.wkbType(), source.sourceCrs())

        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()
        print(features)

        for current, feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            # sshuair begin
            geom = feature.geometry()
            attrs = feature.attributes()
            geom_type = geom.wkbType()

            feature_new = QgsFeature()

            # Point
            if geom_type == 1:
                vertices = geom.asPoint()
                vert_new = wgs2gcj(vertices[0], vertices[1])
                feature_new.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(vert_new[0], vert_new[1])))
            
            # LineString
            elif geom_type == 2:
                vert_new = []
                vertices = geom.asPolyline()
                for pt in vertices:
                    pt_new = wgs2gcj(pt[0], pt[1])
                    vert_new.append(QgsPointXY(pt_new[0], pt_new[1]))
                feature_new.setGeometry(QgsGeometry.fromPolylineXY(vert_new))
            
            # Polygon
            elif geom_type == 3:
                vertices = geom.asPolygon()
                vert_new = []
                for ring in vertices:
                    ring_vert = []
                    for pt in ring:
                        pt_new = wgs2gcj(pt[0], pt[1])
                        ring_vert.append(QgsPointXY(pt_new[0], pt_new[1]))
                    vert_new.append(ring_vert)
                feature_new.setGeometry(QgsGeometry.fromPolygonXY(vert_new))
            
            # MultiPoint
            elif geom_type == 4:
                vert_new = []
                vertices = geom.asMultiPoint()
                for pt in vertices:
                    pt_new = wgs2gcj(pt[0], pt[1])
                    vert_new.append(QgsPointXY(pt_new[0], pt_new[1]))
                feature_new.setGeometry(QgsGeometry.fromMultiPointXY(vert_new))
            
            # MultiLineString
            elif geom_type == 5:
                vertices = geom.asMultiPolyline()
                vert_new = []
                for part in vertices:
                    linestring = []
                    for pt in part:
                        pt_new = wgs2gcj(pt[0], pt[1])
                        linestring.append(QgsPointXY(pt_new[0], pt_new[1]))
                    vert_new.append(linestring)
                feature_new.setGeometry(QgsGeometry.fromMultiPolylineXY(vert_new))

            # MultiPolygon
            elif geom_type == 6:
                vertices = geom.asMultiPolygon()
                vert_new = []
                for part in vertices:
                    poly = []
                    for ring in part:
                        ring_vert = []
                        for pt in ring:
                            pt_new = wgs2gcj(pt[0], pt[1])
                            ring_vert.append(QgsPointXY(pt_new[0], pt_new[1]))
                        poly.append(ring_vert)
                    vert_new.append(poly)
                feature_new.setGeometry(QgsGeometry.fromMultiPolygonXY(vert_new))
            else:
                continue
                
            feature_new.setAttributes(attrs)
            # sshuair end



            # feature = feature+0.1
            # Add a feature in the sink
            sink.addFeature(feature_new, QgsFeatureSink.FastInsert)

            # Update the progress bar
            feedback.setProgress(int(current * total))
            print(feature)

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: dest_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'WGS to GCJ02'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'China Coord Convert'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return WGS2GCJ()
