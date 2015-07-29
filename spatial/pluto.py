import os, glob
import urllib2
import zipfile
import geopandas as gp
import pandas as pd


def read_pluto(dpath=None, bor=None, cols=['geometry', 'BBL']):
    """
    Read the Pluto Data and retrun the five boroughs into 
    one GeoDataFrame.
    
    Parameters
    ----------
    dpath : str, optional
        The path to the PLUTO Datasets(all five boroughs)
        Should be '/PLUTO/'.  Default is './PLUTO'
    
    bor : list, optional
        Specific borough to read
        
    cols : list, optional
        List of columns to keep when building the PLUTO
        data set.  Default is 'geometry' and 'BBL'
        
    Returns
    -------
    
    df : DataFrame
        
    """

    if dpath==None:
        dpath = './PLUTO/'

    print "Reading Pluto files from " + dpath

    if bor==None:
        allFiles = glob.glob(dpath + "/*/*PLUTO.shp")
    else:
        inFile = [dpath + i for i in bor] # get folders
        print "Reading file: " + str(inFile)
        allFiles = [glob.glob(i + "/*PLUTO.shp") for i in inFile] #get files
        allFiles = [j for i in allFiles for j in i]
        
    print "Detected " + str(len(allFiles)) + " files."
    
    # read file and append to master file
    df = gp.GeoDataFrame()
    df_crs = {}
    for i in allFiles:
        print i
        data = gp.GeoDataFrame.from_file(i)
        #cols = ['geometry', 'BBL']
        df_crs = data.crs
        data = gp.GeoDataFrame(data, columns=cols)
        df = df.append(data, ignore_index=True)
    
    df.set_geometry(df.geometry, inplace=True)
    df.crs = df_crs
    
    return df

def download_files(url=None, unzip=True):
    """
    Download Pluto data, unzip and remove old files.
    
    Parameters
    ----------
    url : string, optional
        url to the file to download.  Defaults to all
        PLUTO data here:
        
        http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml
    
    unzip : boolean, optional
        Default set to True.  Set false to just download
        files.
        
    """
    def unzip(fname):
        print "Extracting: ", fname
        with zipfile.ZipFile(fname, "r") as z:
            z.extractall("")
    
        os.remove(fname) # remove .gz file    

    data = urllib2.urlopen(url)
    path, fname = os.path.split(url)
    output = open(fname,'wb')
    output.write(data.read())
    output.close()
    
    if unzip:
        unzip(fname)

def download_all_pluto():
    """
    Download All Pluto shapefiles.  Place them into a folder
    called /PLUTO in the current working directory.
    
    """
    bx = 'http://www.nyc.gov/html/dcp/download/bytes/bx_mappluto_15v1.zip'
    qn = 'http://www.nyc.gov/html/dcp/download/bytes/qn_mappluto_15v1.zip'
    bk = 'http://www.nyc.gov/html/dcp/download/bytes/bk_mappluto_15v1.zip'
    mn = 'http://www.nyc.gov/html/dcp/download/bytes/mn_mappluto_15v1.zip'
    si = 'http://www.nyc.gov/html/dcp/download/bytes/si_mappluto_15v1.zip'
    
    dpath = os.path.join(os.getcwd()+'/PLUTO')
    
    print dpath
    
    if not os.path.exists(dpath):
        os.makedirs(dpath)
        os.chdir(dpath)
        
    sources = [bx, qn, bk, mn, si]
    
    [download_files(url=i) for i in sources]
    
    os.chdir('..')
    
def subset_zip(df, zipCode):
    """
    Subset PLUTO data by the zipcode
    
    Parameters
    ----------
    
    df : GeoDataFrame, required
        Data to be subsetted
    
    zipCode : int, list, required
        Zip code or codes to subset
    
    Returns
    -------
    
    GeoDataFrame
    """
    
    df = df[df['Zip'] == zipCode]
    
    return df
    
