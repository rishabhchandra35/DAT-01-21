import pandas as pd
import numpy as np
import feather

def probe_df(file_path, chunksize = 1000):
  data = {}
  rows = 0
  for chunk in pd.read_csv(file_path, chunksize=chunksize):
    rows += chunk.count()
    for column in chunk.columns:
      if column in data:
        data[column]['null_values'] += chunk[column].isnull().sum()
        if chunk[column].dtypes == int or chunk[column].dtypes == float:
          data[column]['avg_val'] =  (data[column]['avg_val'] + chunk[column].mean()) / 2
      else:                 
        data[column] = {}
        data[column]['null_values'] = chunk[column].isnull().sum()
        data[column]['dtype'] = chunk[column].dtypes
        if chunk[column].dtypes == int or chunk[column].dtypes == float:
          data[column]['avg_val'] = chunk[column].mean()
  return data

def write_df(file_path_read, file_path_write, chunksize = 1000, missing_vals = {}):
  for num, chunk in enumerate(pd.read_csv(file_path_read, chunksize=chunksize)):
    for column in missing_vals:
      chunk[column].fillna(missing_vals[column], inplace=True)
    if num == 0:
      chunk.to_csv(file_path_write, header=True)
    else: 
      chunk.to_csv(file_path_write, header=False)
      
