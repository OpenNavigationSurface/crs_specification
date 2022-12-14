# -*- coding: utf-8 -*-
"""boundcrs_vertical.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UwCCebgRd8EqLxUWPNKyVrWazzCe-0u1

Examples for creating a vertical BoundCRS objects in pyproj.
"""

import os
import sys

!pip install pyproj

import pyproj

pyproj.__version__

pyproj.proj_version_str

pyproj.network.set_network_enabled(active=True)

source_crs_wkt = 'VERTCRS["NOAA Chart Datum",VDATUM["NOAA Chart Datum"],CS[vertical,1],AXIS["gravity-related height (H)",up,LENGTHUNIT["metre",1,ID["EPSG",9001]]]]'
source_crs = pyproj.CRS.from_wkt(source_crs_wkt)

target_crs = pyproj.CRS('EPSG:6319')

"""We need the files to reference in the transformation and will be pulled via FTP for this example."""

from ftplib import FTP
from zipfile import ZipFile
with FTP('ocsftp.ncd.noaa.gov') as ocs_ftp:
  ocs_ftp.login()
  ocs_ftp.cwd('HSTB')
  with open('vdatum.zip', 'wb') as vdatum_zip:
    ocs_ftp.retrbinary('RETR vdatum.zip', vdatum_zip.write)
with ZipFile('vdatum.zip') as vdatum:
  vdatum.extractall()
pyproj.datadir.append_data_dir('vdatum')

"""Make a transformation object"""

pipeline_str = 'proj=pipeline inv step proj=vgridshift grids=core/geoid12b/g2012bu0.gtx step proj=vgridshift grids=TXlaggal01_8301/tss.gtx inv step proj=vgridshift grids=TXlaggal01_8301/mllw.gtx'
mllw_to_NAD83 = pyproj.Transformer.from_pipeline(pipeline_str)

"""Build the pyproj Coordinate Operation Object as a json dict"""

coop_json = {}
coop_json['$schema'] = target_crs.to_json_dict()['$schema']
coop_json['type'] = 'Transformation'
coop_json['name'] = 'MLLW to NAD83(2011)'
coop_json['source_crs'] = source_crs.to_json_dict()
coop_json['target_crs'] = target_crs.to_json_dict()
coop_json['method'] = mllw_to_NAD83.to_json_dict()['method']
params = [{'name': 'Geoid (height correction) model file', 'value': 'core\\geoid12b\\g2012bu0.gtx'},
 {'name': 'TSS (height correction) model file', 'value': 'TXlaggal01_8301\\tss.gtx'},
 {'name': 'MLLW (height correction) model file', 'value': 'TXlaggal01_8301\\mllw.gtx'}]
coop_json['parameters'] = params
coop = pyproj.crs.CoordinateOperation.from_json_dict(coop_json)

"""Build the BoundCRS"""

mllw_as_boundcrs = pyproj.crs.BoundCRS(source_crs, target_crs, coop)
print(mllw_as_boundcrs.to_wkt(version='WKT2_2019', pretty=True))
"""
BOUNDCRS[
    SOURCECRS[
        VERTCRS["NOAA Chart Datum",
            VDATUM["NOAA Chart Datum"],
            CS[vertical,1],
                AXIS["gravity-related height (H)",up,
                    LENGTHUNIT["metre",1,
                        ID["EPSG",9001]]]]],
    TARGETCRS[
        GEOGCRS["NAD83(2011)",
            DATUM["NAD83 (National Spatial Reference System 2011)",
                ELLIPSOID["GRS 1980",6378137,298.257222101,
                    LENGTHUNIT["metre",1]]],
            PRIMEM["Greenwich",0,
                ANGLEUNIT["degree",0.0174532925199433]],
            CS[ellipsoidal,3],
                AXIS["geodetic latitude (Lat)",north,
                    ORDER[1],
                    ANGLEUNIT["degree",0.0174532925199433]],
                AXIS["geodetic longitude (Lon)",east,
                    ORDER[2],
                    ANGLEUNIT["degree",0.0174532925199433]],
                AXIS["ellipsoidal height (h)",up,
                    ORDER[3],
                    LENGTHUNIT["metre",1]],
            USAGE[
                SCOPE["Geodesy."],
                AREA["Puerto Rico - onshore and offshore. United States (USA) onshore and offshore - Alabama; Alaska; Arizona; Arkansas; California; Colorado; Connecticut; Delaware; Florida; Georgia; Idaho; Illinois; Indiana; Iowa; Kansas; Kentucky; Louisiana; Maine; Maryland; Massachusetts; Michigan; Minnesota; Mississippi; Missouri; Montana; Nebraska; Nevada; New Hampshire; New Jersey; New Mexico; New York; North Carolina; North Dakota; Ohio; Oklahoma; Oregon; Pennsylvania; Rhode Island; South Carolina; South Dakota; Tennessee; Texas; Utah; Vermont; Virginia; Washington; West Virginia; Wisconsin; Wyoming. US Virgin Islands - onshore and offshore."],
                BBOX[14.92,167.65,74.71,-63.88]],
            ID["EPSG",6319]]],
    ABRIDGEDTRANSFORMATION["MLLW to NAD83(2011)",
        METHOD["PROJ-based operation method: proj=pipeline inv step proj=vgridshift grids=core/geoid12b/g2012bu0.gtx step proj=vgridshift grids=TXlaggal01_8301/tss.gtx inv step proj=vgridshift grids=TXlaggal01_8301/mllw.gtx"],
        PARAMETERFILE["Geoid (height correction) model file","core\geoid12b\g2012bu0.gtx"],
        PARAMETERFILE["TSS (height correction) model file","TXlaggal01_8301\tss.gtx"],
        PARAMETERFILE["MLLW (height correction) model file","TXlaggal01_8301\mllw.gtx"]]]
"""