import os, shutil
import numpy as np
import json
from dajaxice.decorators import dajaxice_register
from gisweb.config import MEDIA_ROOT, MEDIA_URL

from scripts.extract_shp_table import extract_shp_table
from scripts.conversion import shp_to_kml, convert_geotiff_to_kml, shp_to_tif, shp_to_json, geotiff_to_point_shp, geotiff_to_point_json, convert_coord_to_point_shp
from scripts.spatial_analysis import buffer_shapefile, find_point_inside_feature
from scripts.clip_geotiff_by_shp import clip_geotiff_by_shp
from scripts.data_management import change_geotiff_resolution, color_table_on_geotiff


@dajaxice_register(method='GET')
def remove_loaded_file(request, param):
    Uploaded_file = MEDIA_ROOT + MEDIA_URL + param
    os.remove(Uploaded_file)
    #and remove the associated folder for a file is exists
    try:
        shutil.rmtree('{0}'.format(Uploaded_file[:-4]))
    except:
        pass
    
    
@dajaxice_register(method='GET')
def reproject_shapefile(request, selected_shapefile, shapefile_re_project_epsg, projected_shapefile_name):
    if projected_shapefile_name.split(".")[-1] != "shp":
        projected_shapefile_name = "{0}.shp".format(projected_shapefile_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, projected_shapefile_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        s = 'ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:{2} {0} {1}'.format(MEDIA_ROOT+MEDIA_URL+projected_shapefile_name, MEDIA_ROOT+MEDIA_URL+selected_shapefile+'.shp', shapefile_re_project_epsg)
        os.system(s)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def reproject_geotiff(request, selected_geotiff, geotif_re_project_epsg, projected_geotiff_name):
    if projected_geotiff_name.split(".")[-1] != "tif" or projected_geotiff_name.split(".")[-1] != "tiff":
        projected_geotiff_name = "{0}.tif".format(projected_geotiff_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, projected_geotiff_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        s = "gdalwarp -t_srs 'epsg:{2}' {0} {1}".format(MEDIA_ROOT+MEDIA_URL+selected_geotiff, MEDIA_ROOT+MEDIA_URL+projected_geotiff_name, geotif_re_project_epsg)
        os.system(s)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def extract_shp_table_text(request, selected_vector, text_name):
    if text_name.split(".")[-1] != "txt":
        text_name = "{0}.txt".format(text_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, text_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        extract_shp_table(MEDIA_ROOT+MEDIA_URL+selected_vector+'.shp', MEDIA_ROOT+MEDIA_URL+text_name)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def shapefile_to_kml(request, selected_shp, kml_name):
    if kml_name.split(".")[-1] != "kml":
        kml_name = "{0}.kml".format(kml_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, kml_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        shp_to_kml(MEDIA_ROOT + MEDIA_URL + selected_shp + '.shp', MEDIA_ROOT + MEDIA_URL + kml_name)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def shapefile_to_tif(request, selected_shp, tif_name, shp_to_tif_layer, shp_to_tif_epsg, shp_to_tif_width, shp_to_tif_height, shp_to_tif_ot, shp_to_tif_burn1, shp_to_tif_burn2, shp_to_tif_burn3):
    if tif_name.split(".")[-1] != "tif" or tif_name.split(".")[-1] != "tiff":
        tif_name = "{0}.tif".format(tif_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, tif_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        shp_to_tif(selected_shp, tif_name, shp_to_tif_layer, shp_to_tif_epsg, shp_to_tif_width, shp_to_tif_height, shp_to_tif_ot, shp_to_tif_burn1, shp_to_tif_burn2, shp_to_tif_burn3)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def shapefile_to_json(request, selected_shp, shp_to_json_file, shp_to_json_epsg):
    if shp_to_json_file.split(".")[-1] != "json":
        shp_to_json_file = "{0}.json".format(shp_to_json_file)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, shp_to_json_file)):
        return json.dumps({'status': 'File already exists.'})
    else:
        shp_to_json(selected_shp, shp_to_json_file, shp_to_json_epsg)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def buffer_shp(request, selected_shp, buffer_shp_buffer_range, buffer_shp_out_name):
    if buffer_shp_out_name.split(".")[-1] != "shp":
        buffer_shp_out_name = "{0}.shp".format(buffer_shp_out_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, buffer_shp_out_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        buffer_shp_out_layername = buffer_shp_out_name.split(".shp")[0]
        error = buffer_shapefile(selected_shp, buffer_shp_buffer_range, buffer_shp_out_name, buffer_shp_out_layername)
        return json.dumps({'status': error})


@dajaxice_register(method='GET')
def clip_geotiff_by_shapefile(request, selected_geotiff, selected_shapefile, clipped_geotiff_name):
    if clipped_geotiff_name.split(".")[-1] != "tif" or clipped_geotiff_name.split(".")[-1] != "tiff":
        clipped_geotiff_name = "{0}.tif".format(clipped_geotiff_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, clipped_geotiff_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        clip_geotiff_by_shp(MEDIA_ROOT + MEDIA_URL + selected_geotiff , MEDIA_ROOT + MEDIA_URL + selected_shapefile + '.shp', MEDIA_ROOT + MEDIA_URL + clipped_geotiff_name)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def geotiff_to_kml(request, selected_geotiff, geotiff_to_kml_name):
    if geotiff_to_kml_name.split(".")[-1] != "kml":
        geotiff_to_kml_name = "{0}.kml".format(geotiff_to_kml_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, geotiff_to_kml_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        convert_geotiff_to_kml(selected_geotiff, geotiff_to_kml_name)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def geotiff_resolution(request, selected_geotiff, geotiff_new_x_res, geotiff_new_y_res, geotiff_new_resolution_name):
    if geotiff_new_resolution_name.split(".")[-1] != "tif" or geotiff_new_resolution_name.split(".")[-1] != "tiff":
        geotiff_new_resolution_name = "{0}.tif".format(geotiff_new_resolution_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, geotiff_new_resolution_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        change_geotiff_resolution(selected_geotiff, geotiff_new_x_res, geotiff_new_y_res, geotiff_new_resolution_name)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def tif_to_point_shp(request, selected_geotiff, tif_to_point_shp_name, tif_to_point_shp_epsg):
    if tif_to_point_shp_name.split(".")[-1] != "shp":
        tif_to_point_shp_name = "{0}.shp".format(tif_to_point_shp_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, tif_to_point_shp_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        tif_to_point_shp_layer_name = tif_to_point_shp_name.split(".shp")[0]
        geotiff_to_point_shp(selected_geotiff, tif_to_point_shp_name, tif_to_point_shp_layer_name, tif_to_point_shp_epsg)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def tif_to_point_json(request, selected_geotiff, tif_to_point_json_name, tif_to_point_json_epsg):
    if tif_to_point_json_name.split(".")[-1] != "json":
        tif_to_point_json_name = "{0}.json".format(tif_to_point_json_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, tif_to_point_json_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        geotiff_to_point_json(selected_geotiff, tif_to_point_json_name, tif_to_point_json_epsg)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def coord_to_point_shp(request, selected_coord_text, coord_to_point_shp_separator, coord_to_point_shp_lat_col, coord_to_point_shp_lon_col, coord_to_point_shp_value_col, coord_to_point_shp_name, coord_to_point_shp_epsg):
    if coord_to_point_shp_name.split(".")[-1] != "shp":
        coord_to_point_shp_name = "{0}.shp".format(coord_to_point_shp_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, coord_to_point_shp_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        coord_to_point_shp_layer_name = coord_to_point_shp_name.split(".shp")[0]
        error = convert_coord_to_point_shp(selected_coord_text, coord_to_point_shp_separator, coord_to_point_shp_lat_col, coord_to_point_shp_lon_col, coord_to_point_shp_value_col, coord_to_point_shp_name, coord_to_point_shp_layer_name, coord_to_point_shp_epsg)
        return json.dumps({'status': error})


@dajaxice_register(method='GET')
def color_table_geotiff(request, selected_geotiff, selected_color_table, colored_geotiff_name):
    if colored_geotiff_name.split(".")[-1] != "tif" or colored_geotiff_name.split(".")[-1] != "tiff":
        colored_geotiff_name = "{0}.tif".format(colored_geotiff_name)
    if os.path.isfile('{0}{1}{2}'.format(MEDIA_ROOT, MEDIA_URL, colored_geotiff_name)):
        return json.dumps({'status': 'File already exists.'})
    else:
        color_table_on_geotiff(selected_geotiff, selected_color_table, colored_geotiff_name)
        return json.dumps({'status': 'Done'})


@dajaxice_register(method='GET')
def point_inside_feature(request, selected_vector, point_inside_shapefile_lat, point_inside_shapefile_lon):
    feature_info = find_point_inside_feature(selected_vector, point_inside_shapefile_lat, point_inside_shapefile_lon)
    return json.dumps({'status': feature_info})
