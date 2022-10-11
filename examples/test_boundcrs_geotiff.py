# -*- coding: utf-8 -*-
"""
Testing if we can get back the BoundCRS WKT we put into the BAG.

Test used GDAL 3.4.2 and PROJ 9.0.0.

While the original CRS was recovered, it was stored in a sidecar file as explained here: https://gdal.org/drivers/raster/gtiff.html#georeferencing
"""

import numpy as np
from osgeo import gdal
boundcrs = r'''BOUNDCRS[
    SOURCECRS[
        COMPOUNDCRS["NAD83 / UTM zone 15N + NOAA Chart Datum",
            PROJCRS["NAD83 / UTM zone 15N",
                BASEGEOGCRS["NAD83",
                    DATUM["North American Datum 1983",
                        ELLIPSOID["GRS 1980",6378137,298.257222101,
                            LENGTHUNIT["metre",1]]],
                    PRIMEM["Greenwich",0,
                        ANGLEUNIT["degree",0.0174532925199433]],
                    ID["EPSG",4269]],
                CONVERSION["UTM zone 15N",
                    METHOD["Transverse Mercator",
                        ID["EPSG",9807]],
                    PARAMETER["Latitude of natural origin",0,
                        ANGLEUNIT["degree",0.0174532925199433],
                        ID["EPSG",8801]],
                    PARAMETER["Longitude of natural origin",-93,
                        ANGLEUNIT["degree",0.0174532925199433],
                        ID["EPSG",8802]],
                    PARAMETER["Scale factor at natural origin",0.9996,
                        SCALEUNIT["unity",1],
                        ID["EPSG",8805]],
                    PARAMETER["False easting",500000,
                        LENGTHUNIT["metre",1],
                        ID["EPSG",8806]],
                    PARAMETER["False northing",0,
                        LENGTHUNIT["metre",1],
                        ID["EPSG",8807]]],
                CS[Cartesian,2],
                    AXIS["(E)",east,
                        ORDER[1],
                        LENGTHUNIT["metre",1]],
                    AXIS["(N)",north,
                        ORDER[2],
                        LENGTHUNIT["metre",1]],
                ID["EPSG",26915]],
            VERTCRS["NOAA Chart Datum",
                VDATUM["NOAA Chart Datum"],
                CS[vertical,1],
                    AXIS["gravity-related height (H)",up,
                        LENGTHUNIT["metre",1,
                            ID["EPSG",9001]]]]]],
    TARGETCRS[
        PROJCRS["NAD83(2011) / UTM zone 15N",
            BASEGEOGCRS["NAD83(2011)",
                DATUM["NAD83 (National Spatial Reference System 2011)",
                    ELLIPSOID["GRS 1980",6378137,298.257222101,
                        LENGTHUNIT["metre",1]]],
                PRIMEM["Greenwich",0,
                    ANGLEUNIT["degree",0.0174532925199433]],
                ID["EPSG",6319]],
            CONVERSION["UTM zone 15N",
                METHOD["Transverse Mercator",
                    ID["EPSG",9807]],
                PARAMETER["Latitude of natural origin",0,
                    ANGLEUNIT["degree",0.0174532925199433],
                    ID["EPSG",8801]],
                PARAMETER["Longitude of natural origin",-93,
                    ANGLEUNIT["degree",0.0174532925199433],
                    ID["EPSG",8802]],
                PARAMETER["Scale factor at natural origin",0.9996,
                    SCALEUNIT["unity",1],
                    ID["EPSG",8805]],
                PARAMETER["False easting",500000,
                    LENGTHUNIT["metre",1],
                    ID["EPSG",8806]],
                PARAMETER["False northing",0,
                    LENGTHUNIT["metre",1],
                    ID["EPSG",8807]],
                ID["EPSG",16015]],
            CS[Cartesian,3],
                AXIS["(E)",east,
                    ORDER[1],
                    LENGTHUNIT["metre",1,
                        ID["EPSG",9001]]],
                AXIS["(N)",north,
                    ORDER[2],
                    LENGTHUNIT["metre",1,
                        ID["EPSG",9001]]],
                AXIS["ellipsoidal height (h)",up,
                    ORDER[3],
                    LENGTHUNIT["metre",1,
                        ID["EPSG",9001]]],
            USAGE[
                SCOPE["unknown"],
                AREA["United States (USA) - between 96°W and 90°W onshore and offshore - Arkansas; Illinois; Iowa; Kansas; Louisiana; Michigan; Minnesota; Mississippi; Missouri; Nebraska; Oklahoma; Tennessee; Texas; Wisconsin."],
                BBOX[25.61,-96.01,49.38,-90]],
            REMARK["Promoted to 3D from EPSG:6344"]]],
    ABRIDGEDTRANSFORMATION["MLLW to NAD83(2011)",
        METHOD["PROJ-based operation method: proj=pipeline inv step proj=vgridshift grids=core/geoid12b/g2012bu0.gtx step proj=vgridshift grids=TXlaggal01_8301/tss.gtx inv step proj=vgridshift grids=TXlaggal01_8301/mllw.gtx"],
        PARAMETERFILE["Geoid (height correction) model file","core\geoid12b\g2012bu0.gtx"],
        PARAMETERFILE["TSS (height correction) model file","TXlaggal01_8301\tss.gtx"],
        PARAMETERFILE["MLLW (height correction) model file","TXlaggal01_8301\mllw.gtx"]]]'''


driver = gdal.GetDriverByName('GTiff')
tmp_file = 'boundcrs_test.tif'
ds = driver.Create(tmp_file, 512, 512, 1, gdal.GDT_Byte)
ds.SetGeoTransform([100, 10, 0, 100, 0, -10 ])
ds.SetProjection(boundcrs)
raster = np.ones((512,512))
band = ds.GetRasterBand(1)
band.WriteArray(raster)
ds = None

test = gdal.Open(tmp_file)
crs = test.GetSpatialRef()
print(crs.ExportToWkt(['MULTILINE=YES','Format=WKT2']))
print(test.GetGeoTransform())

