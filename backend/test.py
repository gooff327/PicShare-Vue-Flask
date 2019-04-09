import os
import requests
def test():
    url = 'https://sm.ms/api/upload'
    files = {'jpg':open('./test.jpg','rb')}
    print(requests.post(url,files))
test()