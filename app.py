

# app.py
from flask import Flask, jsonify, request
import yfinance as yf
from flask_cors import CORS
import pandas as pd


# from charts import create_candlestick_chart
# from RNN import get_rnn_predictions
# from LSTM import lstm_forecast

from ElliotWave import calculate_elliott_wave, identify_buy_sell_signals
from BollingerBands import calculate_BB
from MovingAverages import (
    calculate_MA20, calculate_MA50, calculate_MA100, 
    calculate_EMA20, calculate_EMA100, calculate_EMA50,
    calculate_MA2050100, calculate_EMA2050100, calculate_MACD
)
from AverageTrueRange import calculate_atr
from FibonacciRetracement import calculate_fibonacci_retracement

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

@app.route('/indicators', methods=['GET'])
def moving_averages():
    ticker = request.args.get('ticker', 'AAPL')  # Default to 'AAPL' if no ticker is provided
    indicator = request.args.get('indicator', 'MA20')  # Default to 'MA20' if no indicator is provided

    try:
        # Download 6 months of data
        data = yf.download(ticker, period="6mo")
        data.reset_index(inplace=True)
        
        # SIMPLE moving average
        if indicator == 'MA':
            result = calculate_MA2050100(data)
        elif indicator == 'MA20':
            result = calculate_MA20(data)
        elif indicator == 'MA50':
            result = calculate_MA50(data)
        elif indicator == 'MA100':
            result = calculate_MA100(data)

        # EXPOENETIAL MOVING AVERAGES
        elif indicator == 'EMA':
            result = calculate_EMA2050100(data)
        elif indicator == 'EMA20':
            result = calculate_EMA20(data)
        elif indicator == 'EMA50':
            result = calculate_EMA50(data)
        elif indicator == 'EMA100':
            result = calculate_EMA100(data)  

        elif indicator == 'BB20': # Bollinger Bands for 20 days
            result = calculate_BB(data)

        # MACD
        elif indicator == 'MACD':
            result = calculate_MACD(data)

        #Average True Range
        elif indicator == 'ATR':
            result = calculate_atr(data,14)

        #Fibonacci Retracement
        elif indicator == 'FR':
            stock_data = pd.DataFrame(data)
            result = calculate_fibonacci_retracement(stock_data)
            return jsonify(result)
        
        elif indicator == 'EW00':
                    # Perform Elliott Wave analysis
            peaks, troughs, prices, dates = calculate_elliott_wave(data)
            buy_signals, sell_signals = identify_buy_sell_signals(peaks, troughs, prices, dates)
            
            # Debugging print statements
            print("Peaks:", peaks)
            print("Troughs:", troughs)
            print("Prices:", prices)
            print("Dates:", dates)

            # Create a DataFrame with Close Prices, Peaks, and Troughs
            df = pd.DataFrame({'Date': dates, 'Close': prices})
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Ensure dates are in datetime format
            df['Date'] = df['Date'].dt.strftime("%Y-%m-%d")  # Format as string
            
            # df['Peak'] = pd.Series(prices[peaks], index=peaks)
            # df['Trough'] = pd.Series(prices[troughs], index=troughs)

            # Reset index for JSON serialization
            df.reset_index(drop=True, inplace=True)

            # Include buy/sell signals in the result
            result = {
                "data": df.to_dict(orient='records'),
                #.dropna(subset=["Peak", "Trough"], how="all")
                # .dropna(subset=["Peak", "Trough"], how="all").to_dict(orient='records'),
                "buy_signals": [{"date": date, "price": price} for date, price in buy_signals],
                "sell_signals": [{"date": date, "price": price} for date, price in sell_signals]
            }

            return jsonify(result)            

        else:
            return jsonify({"error": f"Indicator '{indicator}' is not supported."}), 400

        # Convert Date to string for JSON response
        result['Date'] = result['Date'].astype(str)
        return jsonify(result.to_dict(orient='records'))

    except Exception as e:
        return jsonify({"error": str(e)}), 400



if __name__ == '__main__':
    app.run(host="0.0.0.0") #app.run(host="0.0.0.0"), so the server is accessible from outside localhost when deployed.