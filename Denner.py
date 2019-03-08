import os
import zipfile
import pandas as pd
import glob
import numpy as np

col_names = ['date', 'unit', 'value']
month = 2
temp = r'C:\Users\olwo7001\Desktop\CH_data\test'
latest_files = []
total=0
for week in range(5,10):
    week='0'*(2-len(str(week))) + str(week)
    list_of_files = glob.glob(r'C:\Users\olwo7001\Desktop\CH_data\Denner\WK-0{week}\*'.format(week=week))

    latest_file = max(list_of_files, key=os.path.getctime)
    # print(latest_file)
    latest_files.append(latest_file)

    for file in glob.glob(latest_file + '\*Umsatz_*'):
        print(file)

        df =  pd.read_csv(file, header=None, sep=';')

        full = df[df[5] == month]

        full = full[full[11] != 0]
        full = full[~((full[11] > 0) & (full[12] < 0))]
        full = full[~((full[11] < 0) & (full[12] > 0))]
        total=total + full[12].sum()

        print(total)


print('*****************************************************')

# full['month'] = full['date'].apply(lambda x: x[4:6])

# full['date'] = full['date'].astype(str)
# Q=0 OR (Q<0 AND V>0) OR (Q>0 AND V<0)


# result = full.groupby(['date']).aggregate({'unit':np.sum, 'value':np.sum})
print(full.info())
# full['len']=full['date'].apply(lambda row: len(str(row)))


