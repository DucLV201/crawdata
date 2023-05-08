import json
import requests
import mysql.connector
from fastapi import FastAPI
#from craw.crawData import get_hotels
app = FastAPI()
    
#Insert 1 trường đơn vào db
@app.get("/InsertField")
def insert_hotel(name_hotel:str, price_hotel:str, star_hotel:str, link_hotel:str):
    # Kết nối và thao tác với cơ sở dữ liệu MySQL
    mydb = mysql.connector.connect(
        host='mysql',
        user='root',
        password='psw123',
        database='hotels',
        port = '3306'
    )
    cursor = mydb.cursor()
    sql = "INSERT INTO hotels (name_hotel, price, star, link) VALUES (%s, %s, %s, %s)"
    val = (name_hotel, price_hotel, star_hotel, link_hotel)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return{"Ok"}

# Lấy dữ liệu mới và cập nhật vào database
@app.get("/CrawAndSave")
def update_hotels():
    
    #Đưa dữ liệu vừa cào vào hotel_new
    hotel_new = []

    response = requests.get('http://craw:9001/CrawHotels')
    data = response.json()
    for row in data:
        hotel_new.append(row)

    #Đưa dữ liệu từ my sql vào hotel_row
    # Kết nối và thao tác với cơ sở dữ liệu MySQL
    mydb = mysql.connector.connect(
        host='mysql',
        user='root',
        password='psw123',
        database='hotels',
        port = '3306'
    )

    cursor = mydb.cursor()
    sql ="SELECT * FROM hotels"
    cursor.execute(sql)

    hotel_old = []
    for row in cursor:
        hotel_old.append({'hotel_name': row[1], 'hotel_price': str(row[2]), 'hotel_star':row[3], 'hotel_link':row[4]})

    

    # Tìm kiếm dữ liệu khác nhau
    new_name = set([row['hotel_name'] for row in hotel_new])
    old_name = set([row['hotel_name'] for row in hotel_old])
    names_to_add = new_name - old_name
    names_to_remove = old_name - new_name
 
    # Thêm dữ liệu mới vào MySQL
    if len(names_to_add) > 0:
        for row in hotel_new:
            if row['hotel_name'] in names_to_add:
                sql = "INSERT INTO hotels (name_hotel, price, star, link) VALUES (%s, %s, %s, %s)"
                val = (row['hotel_name'], row['hotel_price'], row["hotel_star"], row["hotel_link"])
                cursor.execute(sql, val)
                mydb.commit()


    # Xóa dữ liệu cũ ra khỏi MySQL
    if len(names_to_remove) > 0:
        for row in hotel_old:
            if row['hotel_name'] in names_to_remove:
                sql = "DELETE FROM hotels WHERE name_hotel = %s"
                val = (row['hotel_name'],)
                cursor.execute(sql, val)
                mydb.commit()

    # Cập nhật dữ liệu nếu có thay đổi về giá hay số sao
    for crow_row in hotel_new:
        for db_row in hotel_old:
            if crow_row['hotel_name'] == db_row['hotel_name']:
                # Nếu giá khách sạn đã thay đổi, cập nhật dữ liệu mới vào MySQL
                if int(crow_row['hotel_price']) != int(db_row['hotel_price']):
                    sql = "UPDATE hotels SET price = %s WHERE name_hotel = %s"
                    val = (crow_row['hotel_price'], crow_row['hotel_name'])
                    cursor.execute(sql, val)
                    mydb.commit()
                break
                # Nếu số sao khách sạn đã thay đổi, cập nhật dữ liệu mới vào MySQL
                if crow_row['hotel_star'] != db_row['hotel_star']:
                    sql = "UPDATE hotels SET star = %s WHERE name_hotel = %s"
                    val = (crow_row['hotel_star'], crow_row['hotel_name'])
                    cursor.execute(sql, val)
                    mydb.commit()
                break


    mydb.close()
    return {"message": "Data update to MySQL database."}
#Xem sự thay đổi dữ liệu    
@app.get("/StatisData")
def statis_data():
    # Kết nối và thao tác với cơ sở dữ liệu MySQL
    mydb = mysql.connector.connect(
        host='mysql',
        user='root',
        password='psw123',
        database='hotels',
        port = '3306'
    )
    cursor = mydb.cursor()
    sql ="SELECT COUNT(*) FROM hotel_history WHERE action = 'insert'"
    cursor.execute(sql)
    st_insert = cursor.fetchall()

    sql ="SELECT COUNT(*) FROM hotel_history WHERE action = 'update'"
    cursor.execute(sql)
    st_update = cursor.fetchall()

    sql ="SELECT COUNT(*) FROM hotel_history WHERE action = 'delete'"
    cursor.execute(sql)
    st_delete = cursor.fetchall()

    mydb.close()
    return {"Số dữ liệu khách sạn tạo mới": st_insert,
        "Số dữ liệu khách sạn cập nhật": st_update,
        "Số dữ liệu khách sạn đã xóa": st_delete}

#search
@app.get("/search")
def search(kytu: str):
    mydb = mysql.connector.connect(
        host='mysql',
        user='root',
        password='psw123',
        database='hotels',
        port = '3306'
    )

    cursor = mydb.cursor()
    if kytu.isdigit():
      cursor.execute(f"SELECT name_hotel, price, star, link FROM hotels WHERE price = '{kytu}';")
    else:
      cursor.execute(f"SELECT name_hotel, price, star, link FROM hotels WHERE name_hotel LIKE '%{kytu}%';")
    result = cursor.fetchall()

    mydb.close()  
    return{"hotels":result}


@app.get("/search_hotels_by_price_range")
def hotels_by_price_range(min_price: int, max_price: int):
    mydb = mysql.connector.connect(
        host='mysql',
        user='root',
        password='psw123',
        database='hotels',
        port = '3306'
    )

    cursor = mydb.cursor()
    cursor.execute(f"SELECT name_hotel, price, star, link FROM hotels WHERE price >= {min_price} AND price <= {max_price}")
    result = cursor.fetchall()

    mydb.close()  
    return{"hotels":result}

@app.get("/search_hotels_by_star_range")
def hotels_by_star_range(min_star: int, max_star: int):
    mydb = mysql.connector.connect(
        host='mysql',
        user='root',
        password='psw123',
        database='hotels',
        port = '3306'
    )

    cursor = mydb.cursor()
    cursor.execute(f"SELECT name_hotel, price, star, link FROM hotels WHERE star BETWEEN {min_star} AND {max_star}")
    result = cursor.fetchall()

    mydb.close()
    return {"hotels": result}