import numpy as np
import pandas as pd
import pickle

def save_obj(obj, loc ):
    with open(loc, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(loc):
    with open(loc, 'rb') as f:
        return pickle.load(f)

def reverse_dict(my_map):
    inv_map = {v: k for k, v in my_map.items()}
    return inv_map

def convertRow2Matrix(df, index_cols, maps):
    ''' This is a new function: example use:

    vom_np_2 = convertRow2Matrix(vom, ['TRAD_COMM','REG'], [comm_2_num, reg_2_num])

    '''
    df_copy = df.copy()
    df_copy = df_copy.groupby(index_cols).sum().reset_index()

    index_cols_n = [col+'_Number' for col in index_cols]
    for i, col in enumerate(index_cols):
        df_copy[index_cols_n[i]] = df_copy[col].map(maps[i])

    df_mi = df_copy.set_index(index_cols_n)
    df_mi.drop(index_cols, axis=1, inplace=True)

    shape = [len(list(i.keys())) for i in maps]
    output = np.full(shape, -1000.0)

    df_mi.sort_index(inplace=True)

    for i in list(df_mi.index.values):
        output[i] = df_mi.loc[i].values[0]

    print('Number of empty values: ', output[output<0])

    return output

def sort_gtap_data(file):
    # Importing the data
    data_dict = {}
    with open(input_root.format(file)) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if 'Header' in row[0]:
                key = row[2].split('description: ')[1]
                data_dict[key] = {}
                data_dict[key]['header']= row
                data_dict[key]['data'] = []
                print(row)
            else:
                data_dict[key]['data'].append(row)

    # Reformatting the header
    acronym_list = []
    for i in data_dict.keys():
        print(i)
        data_dict[i]['header'][0] = data_dict[i]['header'][0].split('!Header: ')[1]

    # Creating the output folder
    output_folder = output_root.format(file[:-4].lower())
    if not os.path.exists(output_folder):
        print('New Directory Created: '+file[:-4].lower())
        os.makedirs(output_folder)

    # Turning the data into a DataFrame
    for i in data_dict.keys():
        data_dict[i]['data_df'] = pd.DataFrame(data_dict[i]['data'])

    # Saving the data to csv files by the header name
    header_list = []
    for i in data_dict.keys():
        output_file = output_folder + '/'+ data_dict[i]['header'][0] +'.csv'
        data_dict[i]['data_df'].to_csv(output_file)
        header_list.append(data_dict[i]['header'])

    # Saving the data description
    pd.DataFrame(header_list).to_excel(output_root.format(file[:-4]+'_data-description.xlsx'))
