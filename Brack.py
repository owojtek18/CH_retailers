import os
import zipfile
import pandas as pd
import glob
import numpy as np

def lookup(s):
    """
    This is an extremely fast approach to datetime parsing.
    For large data, the same dates are often repeated. Rather than
    re-parse these, we store all unique dates, parse them, and
    use a lookup to convert all dates.
    """
    dates = {date:pd.to_datetime(date, format='%d%m%Y', errors='ignore') for date in s.unique()}
    return s.map(dates)



month = '02'
temp = r'C:\Users\olwo7001\Desktop\CH_data\test'
latest_files = []
prod_files=[]
for week in range(5,10):
    week='0'*(2-len(str(week))) + str(week)
    list_of_files = glob.glob(r'\\lhrnetapp03cifs.enterprisenet.org\rfeprodapp05\InputBackupFiles\CH\Brack_W'
                              r'\Weekly-2019-WK-0{week}\*'.format(week=week)) # * means all if need specific format then *.csv

    latest_file = max(list_of_files, key=os.path.getctime)
    # print(latest_file)
    latest_files.append(latest_file)

    for file in glob.glob(latest_file + '\Report_Nielsen*'):
        print(file)
        # print(colspecs)
        df = pd.read_excel(file, sheet_name='Sheet1')
        print(df.head())
        df['Verkaufsdatum'] = lookup(df['Verkaufsdatum'])
        df['Week_Number'] = df['Verkaufsdatum'].dt.week
        df = df[df['Week_Number'] == int(week)]
        df = df[(df['Verkaufsdatum'] >= '2019-02-01') & (df['Verkaufsdatum'] <= '2019-02-28')]
        prod_files.append(df)
        # print()

full=pd.concat(prod_files)


print('*****************************************************')



# full['date'] = full['date'].astype(str)
# Q=0 OR (Q<0 AND V>0) OR (Q>0 AND V<0)

print(full['Verkauf CHF (inkl. MWSt.)'].sum())
# full=full[full['Verkauf Menge'] != 0]
# full=full[~((full['Verkauf Menge'] > 0)&(full['Verkauf CHF (inkl. MWSt.)'] < 0))]
# full=full[~((full['Verkauf Menge']  < 0)&(full['Verkauf CHF (inkl. MWSt.)'] > 0))]
full=full[((full['Verkauf Menge']  > 0)&(full['Verkauf CHF (inkl. MWSt.)'] > 0))]


# full=full[full['Verkauf Menge'] > 0]
# full.loc['Total']= full.sum()
print(full['Verkauf CHF (inkl. MWSt.)'].sum()*2)
# result = full.groupby(['date']).aggregate({'unit':np.sum, 'value':np.sum})
print(full.info())
# full['len']=full['date'].apply(lambda row: len(str(row)))


