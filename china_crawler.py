from datetime import datetime,timezone,timedelta
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import time
import pytz
import re
from dotenv import load_dotenv
import os 


class Crawler:
    def __init__(self):
        pass

    @staticmethod
    def get_china_data(product_id):
        url = f'https://qiwuprocurementservice.myshoplaza.com/api/search?keyword={product_id.lower()}&page=0&limit=1'
        
        raw_data = requests.get(url).json()
        product_infos = raw_data['data']['products'][0]['variants']
        result_list = [ {'size':product_info['options'][1]['value'],'price':product_info['price']} for product_info in product_infos ]
        sorted_result_list = sorted(result_list, key=lambda x: float(x['size']))
                
        return sorted_result_list

def main(product_id):
    crawler=Crawler()
    china_data=crawler.get_china_data(product_id)
    return china_data

if __name__ == '__main__':
    crawler=Crawler()
    china_data=crawler.get_china_data('MR530AD')
    pprint(china_data)
    
    

