import pandas as pd
import glob
import numpy as np
import os
colspecs = [(9,17),(54,64),(64,74)]

col_names = ['date', 'unit', 'value']

# read into dataframe

month = '02'
list_of_files = glob.glob(r'\\lhrnetapp03cifs.enterprisenet.org\rfeprodapp05\InputBackupFiles\CH\Manor_M\Monthly-2019-MM-0{month}\*'.format(month=month))

latest_file = max(list_of_files, key=os.path.getctime)

files = []

all_input = glob.glob(latest_file + r'\*vk*') + glob.glob(latest_file + r'\*sa*')
# print(glob.glob(r'\\lhrnetapp03cifs.enterprisenet.org\rfeprodapp05\InputBackupFiles\CH\Manor_M\Monthly-2019-MM-002\20190305_0839213921\*vk*'))
for file in all_input:
    print(file)
    df = pd.read_fwf(file, names=col_names, colspecs = colspecs, header=None, index_col=None, encoding='utf8')
    # print(df.info())
    files.append(df)
# for file in glob.glob(r'\\lhrnetapp03cifs.enterprisenet.org\rfeqaapp01\InputFiles\GL\tempfolderSWISS\amavita\wk1\*RA32_*'):
#     print(file)
#     print(colspecs)
#     df = pd.read_fwf(file, names=col_names, colspecs = colspecs, header=None, index_col=None, encoding='utf8')
#     files.append(df)

full=pd.concat(files)
dates= full.date.unique()



# full['value']=full['value'].str.lstrip('0')
# full['value']=full['value'].apply(lambda x: x.replace(',','.').strip())
# full['value']=full['value'].replace(r'', np.nan, regex=True)
# full['value']=full['value'].fillna(0)

# quit()
full.value = full.value.astype(float)
full.unit = full.unit.astype(float)
# Q=0 OR (Q<0 AND V>0) OR (Q>0 AND V<0)
print(full.info())
# full=full[full.unit != 0]
# full=full[~((full.unit > 0)&(full.value < 0))]
full=full[((full.unit >0)&(full.value > 0))]
# full.to_csv(r'\\lhrnetapp03cifs.enterprisenet.org\rfeqaapp01\InputFiles\GL\tempfolderSWISS\cleaned2.txt')
# result = full.groupby(['date']).aggregate({'unit':np.sum, 'value':np.sum})
# result.to_csv(r'\\lhrnetapp03cifs.enterprisenet.org\rfeqaapp01\InputFiles\GL\tempfolderSWISS\cleaned.txt')
full.loc['Total']= full.sum()/100
print(full.loc['Total'])
# print(full.info())
# full['len']=full['date'].apply(lambda row: len(str(row)))

quit()