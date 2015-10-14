import numpy as np

def above_std(val, num=3):
    """
    Function to get values that are within x*std().
    
    Parameters
    ----------
    
    val : Series, required
        Data to calculate the standard deviation
        
    num : int, optional
        Multiplier for the number of standard deviations
        to calculate against a value.  Default is 3
        
    Returns
    -------
    
    result : Series
    """
    result = val[(np.abs(val-val.mean()) <= (num*val.std()))]
    
    return result