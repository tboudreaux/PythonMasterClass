import pandas as pd     # Pandas - module used for large data set analysis
import numpy as np      # Numpy - adds mathematically operations and some new data types


# Define file path to date
sdBCat1_name = '../Data/sdBCatalouge.csv'
sdBCat2_name = '../Data/LessDetailedCatalouge.csv'
spectrum1_name = '../Data/testspectrum.csv'
h5file_name = '../Data/Database.h5'

# Reading in sdBCat2 without pandas
sdBCat2_manual = [x.strip('\n').rsplit() for x in open(sdBCat2_name).readlines()]

# print sdBCat2_manual

# Reading in sdBCat2 with pandas
sdBCat2_pandas = pd.read_csv(sdBCat2_name, delimiter='\t')

# print sdBCat2_pandas

# Reading in sdBCat2 with numpy
sdBCat2_numpy = np.genfromtxt(sdBCat2_name, delimiter='\t')

# print sdBCat2_numpy

"""
Good for different things:
    - Reading in manually will give you the most control over where stuff if placed in array
        - if you have an non rectangular data set this may be the way to go
    - Pandas will read in almost any data set very quickly and allow for more nautral search and query
        using index and column names
        -Handels massive data set memorey allocation for you quite well
    - Will only read in numbers by default
        -reads into a standard list not the more complicated DataFrame
"""

"""
Disadvantages for each:
    Manual:
        - Manual Requires more work and generally a slightly different approach for each data set
        - Sometimes it can be hard to query data as you have to rely on indexes
        - If you have colunm-wise data as opposed to row-wise data a more complicated read in or a reshape is required
    Pandas:
        - Dataframes use a different indexing scheme (loc, iloc as opposed to []) which can make them unwieldly
        - Take up slightly more memory in a raw form
        - When generating or moving dataframes around index colums can get messed up and confusing
    Numpy:
        - Does not read in string data by default
        - similar problems to 2 and 3 for Manual

"""

# HDF5 DATA FORMAT

# N.B Database.h5 is a 4 dimensional data object and therefor requires much more complex read in scheme

test_hdf = {}   # Read individual 3D elements into dictionary
i = 0.001       # Known stat value for 4D keys
while i <= 0.101:
    test_hdf[str(i)] = pd.read_hdf(h5file_name, key=str(i))     # Read in the 3D data files to the dict with key i
    i += 0.001
test_hdf_4D_Panel = pd.Panel4D(data=test_hdf)       # Convert that dictionary to a true Pandas 4D panel

# print test_hdf_4D_Panel

"""
Panels, HDF5, Multi-dimensional Data structures

    Panels are a 3, 4 and higher dimensional data structures based around dataframes
        - a 3d panel = stack of data frames, 4D panel = stack of 3D panels

    HDF5
        -Binary data structure able to store data objects
        -pandas can read and write to HDF5
        -On the fly compression
            -200GB of Light curve data to 50GB of compressed data

"""