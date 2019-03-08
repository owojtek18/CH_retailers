import os
import glob
import pandas as pd

path = r'\\lhrnetapp03cifs.enterprisenet.org\rfeprodapp05\InputBackupFiles\CH\Spar_W\\'
total = pd.DataFrame()

for i in range(5,10):
    os.chdir(path + f'Weekly-2019-WK-00{i}')
    os.chdir(os.listdir()[0])
    for file in glob.glob('Z_EXPO_64*'):
        data = pd.read_csv(file, sep=';', encoding='utf8', header=None)
        total = total.append(data)
total = total.rename(columns={2:'date', 8:'unit', 9:'value'})
total.value = total.apply(lambda x: x.value if x[7] =='#' else -x.value, axis=1)
# total = total.dropna()
# total = total.reset_index(drop=True)
print(total.value.sum())