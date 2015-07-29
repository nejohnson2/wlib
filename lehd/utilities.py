import glob, os 
import pandas as pd

def read_all_data(dpath=None):
    """
    Function to read all LEHD csv files.  Adds a column
    named 'Year' to the dataset.
    
    Parameters
    ----------
    
    dpath : str, optional
        Path to LEHD dataset.  Default is './LEHD_Data/ny_rac/'
        
    Returns
    -------
    
    Dataframe
    
    """
    
    if dpath==None:
        dpath = './LEHD_Data/ny_rac/'
        
    allFiles = glob.glob(dpath + "/*.csv")
    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        print "Reading " + file_
        fname = os.path.split(file_)[1] # get filename
        date = fname[(len(fname)-8):-4] # get date from filename
        df = pd.read_csv(file_,index_col=None, header=0)
        df['Year'] = date # add date to dataframe
        list_.append(df)
    df = pd.concat(list_)  
    
    return df

def sub_year(data, year):
    """
    Subset LEHD by year
    
    Parameters
    ----------
    
    data : DataFrame, required
        LEHD to be subset
    
    year : int, list, required
        Dates to subset
        
    Returns
    -------
    
    result : DataFrame
    """

    if type(year) == list:
        result = data[data['Year'].isin(year)]
        return result
    elif type(year) == int:
        result = data[data['Year'] == year]
        return result
    else:
        print "Error: Unknown type"
        return
    

def sub_county(data, col='h_geocode', county=['005', '047','061','081','085']):
    """
    Subset LEHD data by county number.
    
    Parameters
    ----------
    
    data : DataFrame, required
        Data to subset
    
    col : str, optional
        Column which contains the states index.
        Default is 'h_geocode'
        
    county : int, list, optional
        Three digit county code to subset from LEHD
        data.  Default is 'Bronx', 'Kings'
        'New York', 'Richmond' and 'Queens'
        
    Returns
    -------
    
    result : DataFrame
    """

    data['_'] = [j[2:-10] for i,j in enumerate(data[col].astype(str))]

    df = data[data['_'].isin(county)]
    df.drop('_', axis=1, inplace=True)

    return df   

