import pandas as pd
import glob
import numpy as np
import os
import zipfile
import gzip
import shutil
import ntpath

# col_names = ['date','shop','item', 'unit', 'value']

month ='02'
temp = r'C:\Users\olwo7001\Desktop\CH_data\test'

files = []
list_of_files = glob.glob(r'\\lhrnetapp03cifs.enterprisenet.org\rfeprodapp05\InputBackupFiles\CH\Coop_M\Monthly-2019-M'
                          r'M-0{month}\*'.format(month=month))

latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)
# latest_files.append(latest_file)
total = 0
for file in glob.glob(latest_file+r'\*ra32*.gz'.format(month=month)):
    print(file)
    # print(df.info())
    head, tail = ntpath.split(file)

    with gzip.open(file, 'rb') as f_in:
        with open(os.path.join(temp, tail).replace('.gz',''), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
del f_in, f_out
for file in glob.glob(temp +'\*ra32*'):
    print(file)

    for chunk in  pd.read_csv(file, header=None, sep=';', usecols=[11,12], chunksize=1000000):
        chunk[11] = chunk[11].astype(float)
        chunk[12] = chunk[12].astype(float)

        chunk=chunk[((chunk[11] >0)&(chunk[12] > 0))]
        total= total + chunk[12].sum()

        print(total)



for file in glob.glob(temp +'\*'):
    os.remove(file)




quit()