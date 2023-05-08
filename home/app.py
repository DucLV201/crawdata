from flask import Flask, render_template, request, json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/search_price', methods=['GET', 'POST'])
def search_price():
    min_price = request.form['min_price']
    max_price = request.form['max_price']

    # Gọi API ở đây để lấy kết quả tìm kiếm dựa trên min_price và max_price

    result = requests.get(f'http://mysql_api:9002/search_hotels_by_price_range?min_price={min_price}&max_price={max_price}').json()
    

    return render_template('index.html', result=result)

@app.route('/search_star', methods=['GET', 'POST'])
def search_star():
    min_star = request.form['min_star']
    max_star = request.form['max_star']

    # Gọi API ở đây để lấy kết quả tìm kiếm dựa trên min_star và max_star

    result = requests.get(f'http://mysql_api:9002/search_hotels_by_star_range?min_star={min_star}&max_star={max_star}').json()
    

    return render_template('index.html', result=result)

@app.route('/search', methods=['GET', 'POST'])
def search():
    kytu = request.form['kytu']

    # Gọi API ở đây để lấy kết quả tìm kiếm dựa trên kytu

    result = requests.get(f'http://mysql_api:9002/search?kytu={kytu}').json()
    

    return render_template('index.html', result=result)