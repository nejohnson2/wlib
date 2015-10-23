'''
Collection of functions to cleanup the DSNY data.

This should be turned into a module eventually.

Author:
Nicholas Johnson

'''

import pandas as pd
from datetime import datetime


def read_waste(dpath=None,cols=None, data_types=None, cleaned=True):
    """
    Default waste reader
    
    Parameters
    ----------
    
    dpath : str, required
        Path to waste data.  Default is set to
        
        '../Data/workcomp_extract.csv'
        
    cols : list, 
        columns to subset while importing
    
    dtype : dict,
        Data types for incoming columns
        
    cleaned : boolean
        Run cleaning process - remove na's from
        the time column, remove invalid truck_ids
        and set 'Dump_Time_Stamp' as index
        
    """
    
    # -- set defaults
    if dpath==None:
        dpath = '../Data/workcomp_extract.csv'

    if cols==None:
        cols = ['Tons_Collected', 'Dump_Time_Stamp', 'Section_Code','Truck_ID', 'Material_Type_Code', 'Route_Code']
        
    if data_types==None:
        data_types = {
            'Truck_ID': str,
            'Section_Code': str,
            'Tons_Collected': float,
            'Dump_Time_Stamp': str,
            'Material_Type_Code': int,
            'Route_Code': str 
            }
    
    if cleaned==True:
        print "Reading file from " + dpath
        print "Cleaning data set..."
        df = pd.read_csv(dpath, usecols=cols, dtype=data_types)            
        df = rm_nan_time(df)
        df = rm_truck_id(df)
        df = ts_set_index(df)
        df['Section_Code'] = df['Section_Code'].map(clean_district)
        df = drop_specific_sections(df)
        return df
    else:
        df = pd.read_csv(dpath, usecols=cols, dtype=data_types)

    return df


def clean_district(col):
    """
    Read Waste data
    
    Parameters
    ----------
    
    col : str, required
        This is the column with section names that need
        to be cleaned in order to properly fit the 
        DSNY geography data set.  There are geometries
        which get dropped when merged.
    
    """
    
    col = str(col).strip()
    if col[:2] == 'QS' or col[:2] == 'QN':
        return col[:1] + 'E' + col[2:]
    elif col[:1] == 'M':
        return 'MN' + col[2:]
    elif col[:2] == 'BX':
        return col[:2] + col[-3:]
    elif col[:2] == 'BK':
        if col[:3] == 'BKW':
            return 'BKS' + col[-3:]
        elif col[:3] == 'BKE':
            if col[-3:] in ['091', '092','093', '161','162','171', '172', '173','174','175']:
                return 'BKN' + col[-3:]
            else:
                return 'BKS' + col[-3:]
        else:
            return col[:]
    else:
        return col[:]    

def sep_materials(df, material_type_code):
    """
    Subset data by the various material type codes.
    
    Parameters
    ----------
    
    data : DataFrame, required
        Data to be subsetted
    
    material_type_code : int, required
        Code taken from the DSNY Material Type Code
        explanation.
    """
    
    df = df[df['Material_Type_Code'] == material_type_code]
    
    return df

def rm_truck_id(df):
    """
    Remove rows with truck_ids '9999999'
    
    Parameters
    ----------
    
    df : DataFrame, required
        Data to be cleaned
    """
    
    df = df[~(df['Truck_ID'] == '9999999')]
    
    return df
    
def rm_nan_time(df):
    """
    Remove rows that have 'nan' in time stamps
    
    Parameters
    ----------
    
    df : DataFrame, required
        Data to be cleaned
    """
    
    df.dropna(subset=['Dump_Time_Stamp'], inplace=True)
    
    return df
    
def ts_set_index(df):
    """
    Set the 'Dump_Time_Stamp' columns as the index
    
    Parameters
    ----------
    
    df: DataFrame, required
        Data to be operated on
    """
    print "Removing NaN's from 'Dump_Time_Stamp' first!"
    df = rm_nan_time(df)
    
    def f(x):
        return datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S')
    
    df['Dump_Time_Stamp'] = df['Dump_Time_Stamp'].apply(f)
    
    df.set_index('Dump_Time_Stamp', inplace=True)
    
    return df

def drop_specific_sections(df):
    """
    Remove sections from waste data that
    do not appear in the waste shapefile.

    Parameters
    ----------

    df: DataFrame, required

    """

    drop_cols = ['AFFB02', 'AFFBK', 'AFFBX', 'AFFM03', 'AFFM10', 'AFFMN', 'AFFQN',
       'AFFS02', 'AFFSI', 'BKLC1', 'BKLC2', 'BKLC3', 'BKLC4', 'BXLC1',
       'FKA1', 'MN012', 'MN102', 'MNLC1', 'MNLC2', 'OTHCLN', 'OTHSCH',
       'QEB1', 'QELC1', 'QELC2', 'SILC1', 'SILC2']

    df = df[~df['Section_Code'].isin(drop_cols)]

    return df

def read_raw(dpath=None):
    """
    Read raw sanitation data

    Parameters
    ----------

    dpath: path/to/csv 

    Returns
    -------

    Dataframe
    """

    if dpath==None:
        dpath = '../Data/workcomp_extract.csv'

    df = pd.read_csv(dpath)

    print("Reading Sanitation Data")
    print("Reading:   file = {0}".format(dpath))

    return df