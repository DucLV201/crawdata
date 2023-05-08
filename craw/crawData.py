from typing import List
import pandas
import requests
import json
import re
import time
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

@app.get("/CrawHotels")
def get_hotels():
    # Gửi yêu cầu HTTP đến trang 
    url = "https://www.vietnambooking.com/wp-content/uploads/data_json/hotel/product/country/publish/hotel_post_product_vietnam.json"

    payload={}
    headers = {
    'Cookie': 'PHPSESSID=urft4bktvj857gr6pnqkkot6dc; chk_mobile=computer'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    # Trích xuất thông tin từ HTML của trang web
    data = json.loads(response.text)
    hotels = []
    dem = 0
    for hotel in data: 
        if(dem<20): 
            if hotel["path_1"] == "Đà Nẵng":
                dem= dem +1
                #lấy link thông tin khách sạn
                response1 = requests.get(hotel["url_link"])
                soup = BeautifulSoup(response1.content, "html.parser")
                #lọc ra giá và sao
                price = soup.find('div', class_='price-medium').text
                star =soup.find('span', class_='box-star hotel-star')
                m = re.findall(r'\d', price)
                last_price = ''.join(m)
                n = re.findall(r'fa fa-star', str(star))
                if len(n)== 0:
                    last_star = 1
                else:
                    last_star = len(n)
                time.sleep(0.1)
                hotel_name = hotel["title"]
                hotel_price = last_price
                hotel_star = last_star
                hotel_link = hotel["url_link"]
                    
                hotel_info = {
                        "hotel_name": str(hotel_name),
                        "hotel_price": str(hotel_price),
                        "hotel_star": str(hotel_star),
                        "hotel_link": str(hotel_link)
                    }            
                hotels.append(hotel_info)
    
    return hotels






