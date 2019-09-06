# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 10:03:39 2019

@author: SpencerCollins
"""

#%%
import json
import requests
import sqlite3
import sys
import time
from datetime import datetime

def extractor(json_text, currency):
    # returns Date, Currency_Code, Price
    return datetime.strptime(json_text['time']['updateduk'], '%b %d, %Y at %H:%M BST'),json_text['bpi'][currency]['code'], json_text['bpi'][currency]['rate_float']

def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print(sys.exc_info()[0])
 
    return conn

def timed_execute(secs):
    url = r'https://api.coindesk.com/v1/bpi/currentprice/GBP.json'
    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

    r = requests.get(url, header)
    
    response = json.loads(r.text)
    
    date, curr, price = extractor(response, 'GBP')
    
    conn = create_connection(r'C:\dbs\crypto.db')
    
    query = '''INSERT INTO BTC VALUES(?,?,?)'''
    cursor = conn.cursor()
    cursor.execute(query, (date,curr,price))
    
    query = '''select * from BTC'''
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)
    conn.commit()
    conn.close()
    
    time.sleep(secs)
  
if __name__=='__main__':
    while True:
        print('executing')
        timed_execute(60)

