#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


def probe_df(file_path, chunksize=1000):
    #counter variables to store count of null values and average of each streamed chunk 
    null_sum = 0
    avg_sum = []
    #iterate through each chunk and append relevant info to counter variables
    for chunk in pd.read_csv(file_path, chunksize=chunksize):
        null_sum += chunk.isnull().sum()
        dtypes = chunk.dtypes
        avg_sum.append(chunk.mean())
    
    #calculate mean of all chunks, then convert it to a dictionary
    avg_val = (pd.concat(avg_sum).groupby(level=0).mean()).to_dict()
    
    #convert null totals into a DataFrame and add a dtype column
    df = pd.DataFrame(null_sum, columns=['null values'])
    df['dtype'] = dtypes
    
    #convert dataframe to dictionary
    df_dict = df.to_dict('index')
    
    #if dtype is float or integer, append average value 
    for k, v in df_dict.items():
        if v['dtype'] == int or v['dtype'] == float:
            v['avg_val'] = avg_val[k]

    return df_dict


# In[3]:


def write_df(file_path_read, file_path_write, chunksize=1000, missing_vals=None):
    #create a boolean variable to determine if the chunk requires a header
    first_chunk = True
    #stream in the file using path and chunksize entered as arguments
    for chunk in pd.read_csv(file_path_read, chunksize=chunksize):
        #if missing_vals arguement is entered, iterate over each column of the chunk
        if missing_vals != None:
            for col_name in chunk:
                #if column is int or float, fill missing values with average (from probe_df function)
                if chunk[col_name].dtype == int or chunk[col_name].dtype == float:
                    chunk[col_name] = chunk[col_name].fillna(missing_vals[col_name]['avg_val'])
        
        #if it's the first iteration, include the header when writing to path; else, header=False
        if first_chunk:
            chunk.to_csv(file_path_write, mode='w', header=True, index=False)
            first_chunk = False
        else:
            chunk.to_csv(file_path_write, mode='a', header=False, index=False)


# In[4]:


path = 'https://dat-data.s3.amazonaws.com/taxi.csv'
column_info = probe_df(path, chunksize=500)
column_info


# In[6]:


path = 'https://dat-data.s3.amazonaws.com/taxi.csv'
path_write = 'taxi_fillna.csv'
write_df(path, path_write, chunksize=500, missing_vals=column_info)


# In[7]:


#rerun to check null
probe_df('taxi_fillna.csv', chunksize=500)


# In[ ]:




