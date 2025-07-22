from flask import Flask, render_template, request
import yfinance as yf
import requests
from bs4 import BeautifulSoup

def get_stock_data(stock_name):
    data = yf.Ticker(stock_name)
    hist = data.history(period='1y')
    return hist

def search_web(stock_name):
    url = f'https://www.google.com/search?q={stock_name}+stock+news'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    headlines = [h.text for h in soup.find_all('h3')][:5]
    return headlines

def predict_movement(hist):
    if hist is None or hist.empty:
        return 'No data', None
    close_prices = hist['Close']
    if close_prices[-1] > close_prices[-30]:
        return 'increase', 'next 30 days'
    else:
        return 'decrease', 'next 30 days'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    duration = None
    headlines = []
    stock_name = ''
    if request.method == 'POST':
        stock_name = request.form.get('stock')
        hist = get_stock_data(stock_name)
        headlines = search_web(stock_name)
        prediction, duration = predict_movement(hist)
    return render_template('index.html', prediction=prediction, duration=duration, headlines=headlines, stock_name=stock_name)

if __name__ == '__main__':
    app.run(debug=True)
