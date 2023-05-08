import schedule
import time
import requests

def schedule_craw_hotels():
    response = requests.get('http://mysql_api:9002/CrawAndSAve')
    print("Data scraped and inserted ")

schedule.every().day.at("15:31").do(schedule_craw_hotels)

while True:
    schedule.run_pending(schedule_craw_hotels())
    time.sleep(1)