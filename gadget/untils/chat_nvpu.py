# -*- coding: utf-8 -*-
# Author:w k
import httpx
import json
from urllib.parse import urlencode
import random


#[2901 情人模式]
#[2753 呆萌模式]

headers['Content-Length'] = str(len(str(urlencode(data))))
print(headers['Content-Length'])
a = httpx.post(api_url, data=data, headers=headers)
print(a.json())
