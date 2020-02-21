import pandas as pd
import numpy as np

def get_data(file_path, chunksize):
    """
    parameters
    ------------
    file_path: str, required.
        path to .csv or .xlsx file to read
    chunksize:
        amount of rows to read

    return
    ------------
    iostream of DataFrames
    """
    # creating data as None incase neither of conditions are
    file_type = file_path.split('.')[-1]
    if file_type in ['csv', 'txt']:
        data = pd.read_csv(file_path, chunksize=chunksize)
    elif file_type in ['xlsx']:
        data = pd.read_excel(file_path, chunksize=chunksize)
    else:
        print("Please use either a .csv or .xlsx file type")
        return None
    return data


def probe_df(file_path, chunksize=1000, to_df=False):
    """
    parameters
    ------------
    file_path: str; required
        Location of file to read in.
    chunksize: int; required, default value is 1000
        Size of the chunk to use when streaming in the file.
    
    return
    ------------
    a dictionary encoded in the following way: 
        - each key is the name of a column within your dataset
        - the value for each key is another dictionary with the following key/value pairs:
        - `null values`: number of null values for that column
        - `dtype`: data type for that column
        - `avg_val`: average value for that column ( if numeric, otherwise don't include )
    """
    # get the streams
    data = get_data(file_path, chunksize)
    # create empty Series of sums and initlaize variables
    sums = pd.Series(dtype=np.number)
    nrows = 0
    nulls = 0
    dtypes = pd.Series(dtype='object')
    columns = []
    for chunk in data:
        # get amount of null rows in chunk
        nulls += chunk.isnull().sum()
        # Initializing the sums Series
        if sums.empty:
            sums = chunk.sum(numeric_only=True)
        else:
            sums += chunk.sum(numeric_only=True)
        # remove null rows for mean
        nrows += chunk.shape[0] - chunk[sums.index].isnull().sum()

        # get dtypes and column names
        if dtypes.empty:
            dtypes = chunk.dtypes
            columns = chunk.columns

    # get the average of the dataset for each col
    means = sums / nrows

    # create the dict that describes the dict
    data_dict = {}
    for col in columns:
        data_dict[col] = {}
        data_dict[col]['null values'] = nulls[col]
        data_dict[col]['dtype'] = dtypes[col].name
        if col in means.index:
            data_dict[col]['avg_val'] = means[col]

    if to_df:
        return pd.DataFrame(data_dict.values(), index=data_dict.keys()) 

    return data_dict


# wanted to write a wrapper function but used a pointless variable in chunk_writer
# def counter(x):
#     def wrapper(*args, **kwargs):
#         if wrapper.calls == 0:
#             print('Writing the headers and first chunk')
#             wrapper.calls +=1
#         else:
#             wrapper.calls +=1
#             print('Writing chunk %s' % wrapper.calls)
#         return x(*args, **kwargs)
#     wrapper.calls = 0
#     return wrapper
            


# @counter
def chunk_writer(chunk, file_path, first_chunk, index=False):
    """
    parameters
    chunk: DataFrame,
        chunk of data to write to file_path
    path_of_file: str
        to output data to
    index: cool, default is False.
        if True, will write index of DataFrame to object
    :return
    """
    file_type = file_path.split('.')[-1]
    if file_type in ['csv', 'txt']:
        #if chunk_writer.calls == 1:
        if first_chunk:
            chunk.to_csv(file_path, index=False)
        else:
            chunk.to_csv(file_path, index=False, header=False, mode='a')
    elif file_type in ['xlsx']:
        # if chunk_writer.calls == 1:
        if first_chunk:
            chunk.to_excel(file_path, index=False)
        else:
            writer = pd.ExcelWriter(file_path, engine='openpyxl', mode='a')
            chunk.to_excel(writer, index=False, header=False)

# @counter
def write_df(file_path_read, file_path_write, chunksize=1000, missing_vals=None):
    """
    parameters
    ------------
    file_path_read: str, required 
        location of file to read in.
    file_path_write: str, required 
        location of the file to write the new file out to
    chunksize: int, required, default value is 1000.
        Size of the chunk to use when streaming in the file.
    missing_vals: dict, optional
        accepts a dictionary as an argument with key/value pairs that list the column in the dataset(key) as well as the value to fill 
        missing values with for that column(value).  The values in this dictionary will be used to fill missing values in the file at 
        the location in file_path_read
    """
    data = get_data(file_path_read, chunksize)
    
    # to use a decorator to count how many times chunk_writer was called to see if it was the first chunk
    # ended up making first_chunk variable
    first_chunk = True
    for chunk in data:
        if missing_vals:
            chunk = chunk.fillna(missing_vals)
        chunk_writer(chunk, file_path_write, first_chunk)
        first_chunk = False


if __name__ == '__main__':
    d = probe_df('../data/titanic.csv', chunksize=100)
    print(d)
    x = probe_df('../data/titanic.csv', chunksize=100, to_df=True)
    print(x)
    nas = {'Age': 0, 'Cabin': 'Nope', 'Embarked':'Nope'}
    write_df('../data/titanic.csv', '../data/titanic2.csv', chunksize=100, missing_vals=nas)
    write_df('../data/titanic.csv', '../data/titanic2.txt', chunksize=100, missing_vals=nas)
    write_df('../data/titanic.csv', '../data/titanic2.xlsx', chunksize=100, missing_vals=nas)