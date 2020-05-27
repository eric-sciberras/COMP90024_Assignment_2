import requests
import time


def wait():
    while True:
        try:
            response = requests.get('http://google.com')
            print('Connected to internet')
            break
        except:
            print('No connection')
            time.sleep(3)
