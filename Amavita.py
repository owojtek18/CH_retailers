import os
import zipfile
import pandas as pd
import glob
import numpy as np

colspecs = [(10,18),(38,50),(50,63)]

col_names = ['date', 'unit', 'value']
month = '02'
temp = r'C:\Users\olwo7001\Desktop\CH_data\test'
latest_files = []
prod_files=[]
for week in range(5,10):
    week='0'*(2-len(str(week))) + str(week)
    list_of_files = glob.glob(r'\\lhrnetapp03cifs.enterprisenet.org\rfeprodapp05\InputBackupFiles\CH\Amavita'
                              r'\Weekly-2019-WK-0{week}\*'.format(week=week)) # * means all if need specific format then *.csv

    latest_file = max(list_of_files, key=os.path.getctime)
    # print(latest_file)
    latest_files.append(latest_file)
    list_of_zipped = glob.glob(latest_file + '\*.zip')  # * means all if need specific format then *.csv
    # print(list_of_zipped)
    for f in list_of_zipped:
        print(f)
        with zipfile.ZipFile(f, "r") as zip_ref:
            zip_ref.extractall(temp)

    for file in glob.glob(latest_file + '\*RA32_*'):
        print(file)
        print(colspecs)
        df = pd.read_fwf(file, names=col_names, colspecs=colspecs, header=None, index_col=None, encoding='utf8',
                         dtype= {'date': 'str', 'unit': 'float', 'value': 'float'})
        prod_files.append(df)
        print()

full=pd.concat(prod_files)
print('online_sales')
for file in glob.glob(temp +'\*02Abverk*RA32.txt*'):
    print(file)
    print(colspecs)
    df = pd.read_fwf(file, names=col_names, colspecs = colspecs, header=None, index_col=None, encoding='utf16',
                     dtype= {'date': 'str', 'unit': 'float', 'value': 'float'})

    full=pd.concat([full,df])
    print(full.info())

print('test')

full['month'] = full['date'].apply(lambda x: x[2:4])

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


