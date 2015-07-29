import os, glob
import urllib2
import zipfile

def download_pophu(state=['36']):
    """
    Download the special edition census data which
    has population at the census block level and 
    some information about housing.
    
    Parameters
    ----------
    
    state : list, optional
        Two digit number for which state to download.
        
    """
    
    dpath = './census/'
    if not os.path.exists(dpath):
        os.makedirs(dpath)

    for i in state:
        print i
        
        dpath = dpath + i + '/'
        if not os.path.exists(dpath):
            os.makedirs(dpath)            
            
        url = 'ftp://ftp2.census.gov/geo/tiger/TIGER2010BLKPOPHU/tabblock2010_' + str(i) + '_pophu.zip'
        f = urllib2.urlopen(url)
        fpath = dpath + os.path.split(url)[1]
        print fpath
        output = open(fpath,'wb')
        output.write(f.read())
        output.close()
        
        unzip(dpath, fpath)

def sub_census(data, counties=['005','047','061','081','085']):
    """
    Subset census spatial geometries based on counties.  Default
    returns counties for New York City.
    
    Parameters
    ----------
    
    data : GeoDataFrame, required
        Data to subset
        
    counties : list, optional
        Three digit code to subset the county.  Default
        are NYC counties.
        
    """
    
    df = data[data['COUNTYFP10'].isin(counties)]
    
    return df

def unzip(dpath, fpath):
    zfile = zipfile.ZipFile(fpath)
    zfile.extractall(dpath)
    os.remove(fpath) # remove .zip file
    