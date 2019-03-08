import pandas as pd
import glob
import numpy as np
import os


col_names = ['date','shop','item', 'unit', 'value']

month ='02'

files = []
list_of_files = glob.glob(r'\\lhrnetapp03cifs.enterprisenet.org\rfeprodapp05\InputBackupFiles\CH\Import_M\Monthly-2019-M'
                          r'M-0{month}\*'.format(month=month))

latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)
# latest_files.append(latest_file)
for file in glob.glob(latest_file+r'\IMPO_RA32*'.format(month=month)):
    print(file)

    df = pd.read_csv(file, header=None, sep=';')
    # print(df.info())
    files.append(df)

if len(files) >1:
    full = pd.concat(files)
    dates = full.date.unique()
else:
    full = files[0]


# quit()

full[11] = full[11].apply(lambda x: pd.to_numeric(x, errors='coerce'))
full[10] = full[10].astype(float)
# Q=0 OR (Q<0 AND V>0) OR (Q>0 AND V<0)
print(full.info())
full=full[full[10] != 0]
full=full[~((full[10] > 0)&(full[11] < 0))]
full=full[~((full[10] <0)&(full[11] > 0))]
# ujemne=full[~((full.unit >0)&(full.value > 0))]
# full = full.groupby(['date','shop','item']).aggregate({'unit':np.sum, 'value':np.sum})
full=full[full[10] >0]

print(full[11].sum())
