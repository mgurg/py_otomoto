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

