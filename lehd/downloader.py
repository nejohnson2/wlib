import requests
import os, glob
import urllib2
from bs4 import BeautifulSoup
import gzip
import pandas as pd

def download_specific(state, source, seg='S000', jtype='JT00', version='LODES7'):
    """
    Download all years of data by specifiying the state, the
    source and which type of data you are looking for.  See
    LEHD documentation for more about seg and jtype.  Places
    files in the directory './LEHD_Data'
    
    Parameters
    ----------
    
    state : str, required
        Two letter abbreviation for the state to 
        download eg 'AL' - Alabama
    
    source : str, required
        Options -
            - 'OD' : origin destination
            - 'RAC' : Residence Area Characteristic
            - 'WAC' : workplace Area Characteristic

    seg : str, optional
         Segment of the workforce, can have the values of 'S000', 'SA01', 
         'SA02', 'SA03', 'SE01', 'SE02', 'SE03', 'SI01', 'SI02', or 'SI03'.
         Default is 'SOOO'.
         
         See LEHD documentations :
         http://lehd.ces.census.gov/data/lodes/LODES7/LODESTechDoc7.1.pdf
    
    jtype : str, optional
        Job Type, can have a value of 'JT00' for All Jobs, 'JT01' for 
        Primary Jobs, 'JT02' for All Private Jobs, 'JT03' for Private 
        Primary Jobs, 'JT04' for All Federal Jobs, or 'JT05' for Federal 
        Primary Jobs.  Default is 'JT00'
        
        See LEHD documentations :
        http://lehd.ces.census.gov/data/lodes/LODES7/LODESTechDoc7.1.pdf
         
    version : str, optional
        Either LODES7 or LODES5.  Default is LODES7
    """
    url = 'http://lehd.ces.census.gov/data/lodes/' + version + '/' + state.lower() + '/' + source.lower() + '/'
    page = requests.get(url) # get the page
    soup = BeautifulSoup(page.content, 'html.parser') # make the page beautiful
    samples = soup.find_all("a") # get all links on the page

    if source.lower() == 'od':
        print "This is not working"
        return
    else:
        f = [a.attrs['href'] for a in samples[5:]]
        ff = state.lower() + '_' + source.lower() + '_' + seg + '_' + jtype + '_'

    # compare all links on the page to the desired links (with all dates)
    index = []
    for i in f:
        if ff == i[:-11]:
            index.append(i)

    # build download url
    files = [url + i for i in index]
    
    dpath = './LEHD_Data/'
    
    if not os.path.exists(dpath):
        os.makedirs(dpath)
        
    dpath = dpath + state + '_' + source + '/'
    if not os.path.exists(dpath):
        os.makedirs(dpath)

    for i in files:
        print i
        f = urllib2.urlopen(i)
        fpath = dpath + os.path.split(i)[1]
        output = open(fpath,'wb')
        output.write(f.read())
        output.close()
        
        unzip(fpath)
    

def unzip(fpath):
    """
    Unzip the new downloaded file and
    remove the old '.gz' file
    
    Parameters
    ----------
    
    fpath : str, required
        Path of the file to unzip and
        remove
    
    """
    inF = gzip.GzipFile(fpath, 'rb')
    s = inF.read()
    inF.close()

    outF = file(fpath[:-3], 'wb')
    outF.write(s)
    outF.close()

    os.remove(fpath) # remove .gz file        

