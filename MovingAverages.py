import pandas as pd

#SIMPLE MOVING AVERAGES
def calculate_MA2050100(data):
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA100'] = data['Close'].rolling(window=100).mean()
    result = data[['Date', 'Close', 'MA20', 'MA50', 'MA100']].dropna().reset_index()
    return result

def calculate_MA20(data):
     data['MA20'] = data['Close'].rolling(window=20).mean()
     result = data[['Date','Close', 'MA20']].dropna().reset_index()
     return result

def calculate_MA50(data):
     data['MA50'] = data['Close'].rolling(window=50).mean()
     result = data[['Date','Close', 'MA50']].dropna().reset_index()
     return result

def calculate_MA100(data):
      data['MA100'] = data['Close'].rolling(window=100).mean()
      result = data[['Date','Close', 'MA100']].dropna().reset_index()
      return result

#EXPONENTIAL MOVING AVERAGES
def calculate_EMA2050100(data):
     data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
     data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
     data['EMA100'] = data['Close'].ewm(span=100, adjust=False).mean()
     result = data[['Date', 'Close', 'EMA20', 'EMA50', 'EMA100']].dropna().reset_index()
     return result

def calculate_EMA20(data):
    data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
    result = data[['Date','Close', 'EMA20']].dropna().reset_index(drop=True)
    
    return result

def calculate_EMA50(data):
    data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
    result = data[['Date','Close', 'EMA50']].dropna().reset_index(drop=True)
  
    return result

def calculate_EMA100(data):
    data['EMA100'] = data['Close'].ewm(span=100, adjust=False).mean()
    result = data[['Date','Close', 'EMA100']].dropna().reset_index(drop=True)
   
    return result

#Moving Average COnvergance Divergence
def calculate_ema(data, window):
    """
    Calculate Exponential Moving Average (EMA).

    Args:
        data (pd.Series): The closing price series.
        window (int): The number of periods for EMA.

    Returns:
        pd.Series: EMA values.
    """
    return data.ewm(span=window, adjust=False).mean()

def calculate_MACD(data):
    # Ensure Date is in datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Calculate MACD components
    ema_12 = calculate_ema(data['Close'], 12)
    ema_26 = calculate_ema(data['Close'], 26)
    macd = ema_12 - ema_26
    signal_line = macd.ewm(span=9, adjust=False).mean()

    # Add MACD and Signal Line to the DataFrame
    data['MACD'] = macd
    data['Signal_line'] = signal_line

    # Only return Date, Close, MACD, and Signal_line after calculation
    result = data[['Date', 'Close', 'MACD', 'Signal_line']].dropna().reset_index(drop=True)
    return result


     