# Stock Predictor Command-line Tool
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

def main():
    stock_name = input('Enter Stock Ticker (e.g., AAPL): ')
    print('Fetching data...')
    hist = get_stock_data(stock_name)
    print('Recent news headlines:')
    headlines = search_web(stock_name)
    for h in headlines:
        print('-', h)
    prediction, duration = predict_movement(hist)
    print(f'Prediction: The stock price may {prediction}.')
    if prediction != "No data":
        print(f'Recommended buy/sell window: {duration}')
if __name__ == '__main__':
    main()
