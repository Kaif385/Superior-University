from flask import Flask, render_template, jsonify, request
import yfinance as yf
import requests
import datetime

app = Flask(__name__)

def get_data_for_symbol(symbol):
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.fast_info.last_price
        previous = ticker.fast_info.previous_close
        
        if price is None or previous is None:
            return None

        change_percent = ((price - previous) / previous) * 100
        
        display_symbol = symbol
        if 'GSPC' in symbol: display_symbol = 'S&P 500'
        elif 'DJI' in symbol: display_symbol = 'Dow Jones'
        elif 'IXIC' in symbol: display_symbol = 'Nasdaq'

        return {
            'symbol': display_symbol,
            'price': round(price, 2),
            'change': round(change_percent, 2)
        }
    except:
        return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_market_summary')
def get_market_summary():
    indices = ['^GSPC', '^DJI', '^IXIC']
    data = []
    for index in indices:
        result = get_data_for_symbol(index)
        if result:
            data.append(result)
    return jsonify(data)

@app.route('/get_stock_price/<path:ticker_symbol>')
def get_stock_price(ticker_symbol):
    try:
        data = get_data_for_symbol(ticker_symbol.upper())
        if data:
            data['timestamp'] = datetime.datetime.now().strftime("%H:%M:%S")
            data['symbol'] = ticker_symbol.upper() 
            return jsonify(data)
        else:
            return jsonify({'error': 'Symbol not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/search')
def search_symbol():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=5&newsCount=0"
        response = requests.get(url, headers=headers)
        data = response.json()
        
        suggestions = []
        if 'quotes' in data:
            for item in data['quotes']:
                if 'symbol' in item:
                    suggestions.append({
                        'symbol': item['symbol'],
                        'name': item.get('shortname', item.get('longname', ''))
                    })
        return jsonify(suggestions)
    except Exception as e:
        print("Search Error:", e)
        return jsonify([])

app.run(debug=True)