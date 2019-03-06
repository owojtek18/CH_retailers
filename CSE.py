import os
import zipfile
import pandas as pd
import glob
import numpy as np

colspecs = [(8,18),(36,47),(47,60)]

col_names = ['date', 'unit', 'value']
month = '02'
temp = r'C:\Users\olwo7001\Desktop\CH_data\test'
latest_files = []
prod_files=[]
for week in range(5,10):
    week='0'*(2-len(str(week))) + str(week)
    list_of_files = glob.glob(r'\\lhrnetapp03cifs.enterprisenet.org\rfeprodapp05\InputBackupFiles\CH\CSE'
                              r'\Weekly-2019-WK-0{week}\*'.format(week=week)) # * means all if need specific format then *.csv

    latest_file = max(list_of_files, key=os.path.getctime)
    # print(latest_file)
    latest_files.append(latest_file)

    for file in glob.glob(latest_file + '\*RA32_*'):
        print(file)
        print(colspecs)
        df = pd.read_fwf(file, names=col_names, colspecs=colspecs, header=None, index_col=None, encoding='utf8',
                         dtype={'date': 'str', 'unit': 'float', 'value': 'float'})
        prod_files.append(df)
        print()

full=pd.concat(prod_files)


print('*****************************************************')

full['month'] = full['date'].apply(lambda x: x[4:6])

# full['date'] = full['date'].astype(str)
# Q=0 OR (Q<0 AND V>0) OR (Q>0 AND V<0)

full = full[full['month'] == month]

full=full[full.unit != 0]
full=full[~((full.unit > 0)&(full.value < 0))]
full=full[~((full.unit < 0)&(full.value > 0))]
# full=full[((full.unit > 0)&(full.value > 0))]


# full=full[full.unit > 0]
# full.loc['Total']= full.sum()
print(full['value'].sum())
# result = full.groupby(['date']).aggregate({'unit':np.sum, 'value':np.sum})
print(full.info())
# full['len']=full['date'].apply(lambda row: len(str(row)))


