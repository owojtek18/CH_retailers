import pandas as pd
import glob
import numpy as np
import os
import time
# x1 = open(working_dir+r'\\' + 'X1W'+str(yy)+str(week)+'.DAT', "w", encoding='ansi')
def lookup(s):
    """
    This is an extremely fast approach to datetime parsing.
    For large data, the same dates are often repeated. Rather than
    re-parse these, we store all unique dates, parse them, and
    use a lookup to convert all dates.
    """
    dates = {date:pd.to_datetime(date) for date in s.unique()}
    return s.map(dates)

month = '02'
nr=0
prod_files=[]
test=0
for week in range(5,10):
    week='0'*(2-len(str(week))) + str(week)
    list_of_files = glob.glob(r'\\lhrnetapp03cifs.enterprisenet.org\rfeprodapp05\InputBackupFiles\CH\Volg\Weekly-2019-WK-0{week}\*'.format(week=week)) # * means all if need specific format then *.csv
    # list_of_files = glob.glob(
    #     r'C:\Users\olwo7001\Desktop\CH_data\Weekly-2019-WK-0{week}\*'.format(
    #         week=week))  # * means all if need specific format then *.csv

    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    # print(latest_file)

    nr = nr + 1

    for file in glob.glob(latest_file + r'\KW*'):

        print(file)
        data = {'data': [],'shop':[], 'volume': [], 'value': []}
        with open(file, encoding='utf8') as f:
            dataa = 0
            volume = 0
            value = 0
            for n,r in enumerate(f):
                if r[0:7] == 'E2WPU01':
                    dataa = r[63:71]
                    # print(r)
                if r[0:7] == 'EDI_DC4':
                    shop = r[193:199]
                    # print(r)
                if r[0:7] == 'E2WPU02':
                    volume = r[108:128]
                    value = r[144:164]
                else:
                    continue
                data['data'].append(dataa)
                data['shop'].append(shop)
                data['volume'].append(volume)
                data['value'].append(value)
                # if n >1000:
                #     break
        print(time.time())
        volg_data = pd.DataFrame.from_dict(data)
        volg_data.volume = volg_data.volume.astype(float)
        volg_data.value = volg_data.value.astype(float)
        print(time.time())
        volg_data['data'] = lookup(volg_data['data'])
        # volg_data['data'] = volg_data['data'].apply(lambda x: pd.to_datetime(x, format='%Y%m%d', errors='ignore'))
        volg_data['Week_Number'] = volg_data['data'].dt.week
        print(time.time())
        volg_data['sample'] = volg_data['shop'].apply(lambda x: x[0:3])
        volg_data = volg_data[volg_data['sample'] == '010']
        volg_data = volg_data[volg_data['Week_Number']==int(week)]
        print(time.time())
        # print()
        # volg_data = volg_data[((volg_data.volume > 0) & (volg_data.value > 0))]
        print(time.time())
        volg_data = volg_data[(volg_data['data'] >= '2019-02-01') & (volg_data['data'] <= '2019-02-28')]
        # volg_data.loc['Total'] = volg_data.sum()
        # print(volg_data.loc['Total','value'])
        test=test+volg_data['value'].sum()
        print(test)
        result = volg_data.groupby(['data', 'shop']).aggregate({'value': np.sum, 'volume': np.sum})
        # print(r'C:\Users\olwo7001\Desktop\CH_data\cleaned_{nr}.txt'.format(nr=nr))
        # result.to_csv(r'C:\Users\olwo7001\Desktop\CH_data\cleaned_{nr}.txt'.format(nr=nr), encoding='ansi', header=None)



        prod_files.append(volg_data)

# full_volg_data=pd.concat(prod_files)




# volg_data = volg_data[volg_data.volume != 0]
# volg_data = volg_data[~((volg_data.volume > 0) & (volg_data.value < 0))]
# volg_data = volg_data[~((volg_data.volume < 0) & (volg_data.value > 0))]
# volg_data = volg_data[volg_data.volume > 0]





    # if n>10:
    #     print(data)
    #     break

# quit()