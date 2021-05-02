import os
import pandas as pd

root_dir = 'Stock/chinafin_dta' # root_dir也可为'Stock/cntop10_dta'

file_list = os.listdir(root_dir)

for each_file in file_list:
    data = pd.io.stata.read_stata(root_dir+'/'+each_file)
    each_file = each_file.split('.')
    data.to_csv('Stock/chinafin_csv/'+each_file[0]+'.csv',encoding='utf-8')

# data = pd.read_csv('Stock/CIRRE_OPERATINGDATA1.csv')

# with open('Stock/codes.txt', 'a') as f:
#     num = 371
#     for i in range(num):
#         f.write(str(data['Symbol'][i]) + ' ')