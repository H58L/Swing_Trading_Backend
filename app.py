

# app.py
from flask import Flask, jsonify, request
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/stock', methods=['GET'])
def get_stock_data():
    stock_ticker = request.args.get('ticker', 'RELIANCE.NS')  # Default to Reliance , Chnage this to a state
    period = request.args.get('period', '1mo')  # Default to 1 month if not provided

    try:
        stock = yf.Ticker(stock_ticker)
        stock_info = stock.history(period=period)  # Fetch data based on selected period

        if not stock_info.empty:
            stock_data = {
                'dates': stock_info.index.strftime('%Y-%m-%d').tolist(),  # Convert dates to strings
                'open': stock_info['Open'].tolist(),
                'high': stock_info['High'].tolist(),
                'low': stock_info['Low'].tolist(),
                'close': stock_info['Close'].tolist(),
                'volume': stock_info['Volume'].tolist(),
            }
            return jsonify(stock_data)
        else:
            return jsonify({'error': 'No data found for the given ticker'}), 404

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/support', methods=['GET'])
def calculate_support_resistance():
    # Get the ticker from the query parameters
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Ticker parameter is required"}), 400

    # Fetch historical data
    try:
        stock_data = yf.download(ticker, period='1mo', interval='1d')
        
        # Drop any rows with missing data
        stock_data = stock_data.dropna()

        # Ensure data is available
        if stock_data.empty:
            return jsonify({"error": "No data available for the specified period"}), 404

        # Get the latest day's high, low, and close prices
        high = float(stock_data['High'].iloc[-1])
        low = float(stock_data['Low'].iloc[-1])
        close = float(stock_data['Close'].iloc[-1])

        # Calculate pivot point
        pivot_point = (high + low + close) / 3

        # Calculate support and resistance levels
        range_ = high - low
        resistances = [pivot_point + i * range_ for i in range(1, 6)]
        supports = [pivot_point - i * range_ for i in range(1, 6)]

        # Prepare the response
        response = {
            "ticker": ticker,
            "pivot_point": round(pivot_point, 2),
            "resistances": [round(r, 2) for r in resistances],
            "supports": [round(s, 2) for s in supports]
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0") #app.run(host="0.0.0.0"), so the server is accessible from outside localhost when deployed.
