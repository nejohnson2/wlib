import geopandas as gp
import pandas as pd
from geopandas.tools import sjoin
from shapely.geometry import Point

def spatial_join(sm_geom, lg_geom):
    """
    Spatially join two geographies adding data from
    the larger geometry to the smaller.  Then add the
    geometry from the smaller geographical unit back
    onto the new dataset one.  Returns a GeoDataFrame.
    
    Parameters
    ----------
    sm_geom : GeoDataFrame
        GeoDataFrame to receive data

    lg_geom : GeoDataFrame
        Large GeoDataFrame to apply data

    """
    sm_original = sm_geom
    
    sm_geom = sm_geom.to_crs(lg_geom.crs)
    
    sm_geom['geometry'] = sm_geom['geometry'].centroid

    df = sjoin(sm_geom, lg_geom, how="left", op="within")
    
    df.drop(['geometry', 'index_right'], axis=1, inplace=True)
    
    df = df.join(pd.DataFrame(sm_original['geometry'], columns=['geometry']))

    return df
    
def join_files(dpath):
    """
    Get all .shp files and join them into
    one shapefile.
    
    Parameters
    ----------
    
    dpath : str, required
        Path to folder
        
    Return
    ------
    
    df : GeoDataFrmae
        
    """
    files = glob.glob(os.path.join(dpath + '/*.shp'))
    
    df = gp.GeoDataFrame()
    df_crs = {}
    for i in files:
        _ = gp.GeoDataFrame.from_file(i)
        df_crs = _.crs
        df = df.append(_, ignore_index=True)
    
    df.set_geometry(df.geometry, inplace=True)
    df.crs = df_crs
    
    return df
    
def create_point_from_lat_lon(lat, lon):
    """Convert Lat/Lon corrdinates into a geometry object"""

    return Point(lat,lon)