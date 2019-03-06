import pandas as pd
import glob
import numpy as np
import os
colspecs = [(6,14),(211,216),(216,226)]

col_names = ['date', 'unit', 'value']

# read into dataframe
month = '02'
list_of_files = glob.glob(r'\\lhrnetapp03cifs.enterprisenet.org\rfeprodapp05\InputBackupFiles\CH\Douglas_M\Monthly-2019-MM-0{month}\*'.format(month=month))

latest_file = max(list_of_files, key=os.path.getctime)

files = []
for file in glob.glob(latest_file + r'\IRI_SALES*'):
    print(file)
    # print(colspecs)
    df = pd.read_fwf(file, names=col_names, colspecs = colspecs, header=None, index_col=None, encoding='utf8')
    # print(df.info())
    files.append(df)
# for file in glob.glob(r'\\lhrnetapp03cifs.enterprisenet.org\rfeqaapp01\InputFiles\GL\tempfolderSWISS\amavita\wk1\*RA32_*'):
#     print(file)
#     print(colspecs)
#     df = pd.read_fwf(file, names=col_names, colspecs = colspecs, header=None, index_col=None, encoding='utf8')
#     files.append(df)

if len(files) >1:
    full = pd.concat(files)
    dates = full.date.unique()
else:
    full = files[0]



full['value']=full['value'].str.lstrip('0')
full['value']=full['value'].apply(lambda x: x.replace(',','.').strip())
full['value']=full['value'].replace(r'', np.nan, regex=True)
full['value']=full['value'].fillna(0)
full.to_csv(r'C:\Users\olwo7001\Desktop\CH_data\test\cleaned.txt')
# quit()
full.value = full.value.astype(float)
full.unit = full.unit.astype(float)
# Q=0 OR (Q<0 AND V>0) OR (Q>0 AND V<0)
print(full.info())
# full=full[full.unit != 0]
# full=full[~((full.unit > 0)&(full.value < 0))]
full=full[((full.unit >0)&(full.value > 0))]

# result = full.groupby(['date']).aggregate({'unit':np.sum, 'value':np.sum})
# result.to_csv(r'\\lhrnetapp03cifs.enterprisenet.org\rfeqaapp01\InputFiles\GL\tempfolderSWISS\cleaned.txt')
full.loc['Total']= full.sum()/100
print(full.loc['Total'])
# print(full.info())
# full['len']=full['date'].apply(lambda row: len(str(row)))

quit()