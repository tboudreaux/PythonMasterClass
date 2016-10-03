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