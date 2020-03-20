# -*- coding: utf-8 -*-
import os
import io
import json
import re
from timeit import default_timer as timer

tstart = timer()

with open('D:\Python\py_otomoto\scrapy_otomoto\scrapy_otomoto\spiders\page.html', 'r', encoding="utf-8") as myfile:
  data = myfile.read()

#regex - 0.0034
# pattern = re.compile(r"""(GPT.targeting = )(.*?);""")
# result = re.search(pattern, data)
# car_json = json.loads(result.group(2))


# python - 0.026
start = data.find('GPT.targeting = ')+len('GPT.targeting = ')
stop = data.find(';', start)
json_data = data[start:stop]
car_json = json.loads(json_data)


print(car_json)
print(car_json['features'])

end = timer()
print('Time: '+ str(end - tstart))


import json 
import pandas as pd 
from pandas.io.json import json_normalize 

# https://medium.com/@amirziai/flatten-json-on-python-package-index-pypi-9e4951693a5a

# def flatten_json(y):
#     out = {}

#     def flatten(x, name=''):
#         if type(x) is dict:
#             for a in x:
#                 flatten(x[a], name + a + '_')
#         elif type(x) is list:
#             i = 0
#             for a in x:
#                 flatten(a, name + str(i) + '_')
#                 i += 1
#         else:
#             out[name[:-1]] = x

#     flatten(y)
#     return out

# with open('y.json') as f: 
#     d = json.load(f) 
    
# flat = flatten_json(d)    
    
    
# yaris = json_normalize(flat) 
# yaris.head(3) 
