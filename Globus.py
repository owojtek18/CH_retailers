import pandas as pd
import glob
import numpy as np
import os
colspecs = [(8,16),(25,28),(28,41),(41,49),(49,59)]

col_names = ['date','shop','item', 'unit', 'value']

month ='02'

files = []
list_of_files = glob.glob(r'\\lhrnetapp03cifs.enterprisenet.org\rfeprodapp05\InputBackupFiles\CH\Globus_M\Monthly-2019-M'
                          r'M-0{month}\*'.format(month=month))

latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)
# latest_files.append(latest_file)
for file in glob.glob(latest_file+r'\GL32*'.format(month=month)):
    print(file)
    # print(colspecs)
    df = pd.read_fwf(file, names=col_names, colspecs = colspecs, header=None, index_col=None, encoding='utf8')
    # print(df.info())
    files.append(df)

if len(files) >1:
    full = pd.concat(files)
    dates = full.date.unique()
else:
    full = files[0]


full=full[~full.shop.isin([121,122,123,125,126,167,128,130,135,136,138,140,163,166,371,372,373,374,375,376,377,378])]
# quit()
full.value = full.value.astype(float)
full.unit = full.unit.astype(float)
# Q=0 OR (Q<0 AND V>0) OR (Q>0 AND V<0)
print(full.info())
full=full[full.unit != 0]
full=full[~((full.unit > 0)&(full.value < 0))]
full=full[~((full.unit <0)&(full.value > 0))]
# ujemne=full[~((full.unit >0)&(full.value > 0))]
full = full.groupby(['date','shop','item']).aggregate({'unit':np.sum, 'value':np.sum})
full=full[full.unit >0]


# uj
full.loc['Total']= full.sum()

print(full.loc['Total'])


quit()