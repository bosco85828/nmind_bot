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
        url = f'https://qiwuprocurementservice.myshoplaza.com/api/search?keyword={product_id.lower()}&page=0&limit=30'
        
        raw_data = requests.get(url).json()
        for data in raw_data['data']['products'] :             
            if data['brief'] == product_id :                 
                product_infos = data['variants']
                break
        else : 
            return None
        
        result_list = []
        
        for product_info in product_infos:
            try : 
                price =int(((float(product_info['price']) + 5) * 4.55 ) + 100)
            except : 
                price = None
            
            size = [ option for option in product_info['options'] if option['name'] == 'Size'][0]

            result_list.append(
                {
                    'size':size['value'],
                    'price':price
                }
            )
        print(result_list)
        # result_list = [ {'size':product_info['options'][1]['value'],'price':float(product_info['price'])} for product_info in product_infos ]
        
        sorted_result_list = sorted(result_list, key=lambda x: x['size'])
                
        return sorted_result_list

def main(product_id):
    crawler=Crawler()
    china_data=crawler.get_china_data(product_id)
    return china_data

if __name__ == '__main__':
    crawler=Crawler()
    china_data=crawler.get_china_data('B75807')
    pprint(china_data)
    
    

