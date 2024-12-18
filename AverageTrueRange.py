import pandas as pd
# def calculate_atr(stock_data, window=14):
#     """
#     Calculate Average True Range (ATR).

#     Args:
#         stock_data (pd.DataFrame): Dataframe containing 'High', 'Low', and 'Close' prices.
#         window (int): Moving average window size (default is 14).

#     Returns:
#         pd.Series: Average True Range values for the dataset.
#     """
#     high = stock_data['High']
#     low = stock_data['Low']
#     close = stock_data['Close']

#     # True Range (TR)
#     tr1 = high - low
#     tr2 = abs(high - close.shift(1))
#     tr3 = abs(low - close.shift(1))

#     true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

#     # Average True Range (ATR)
#     atr = true_range.rolling(window=window).mean()

#     return atr

def calculate_atr(stock_data, window):
    """
    Calculate Average True Range (ATR).
    
    Args:
        stock_data (pd.DataFrame): DataFrame containing 'High', 'Low', and 'Close' prices.
        window (int): Rolling window size for ATR calculation (default is 14).

    Returns:
        pd.DataFrame: DataFrame with 'Date' and 'ATR' columns.
    """
    high = stock_data['High']
    low = stock_data['Low']
    close = stock_data['Close']

    # True Range (TR)
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))

    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # Average True Range (ATR)
    atr = true_range.rolling(window=window).mean()

    # Create a new DataFrame with Date and ATR
    atr_data = pd.DataFrame({
        'Date': stock_data['Date'],
        'Close': stock_data['Close'],
        'ATR': atr
    })

    # Remove rows with NaN values (which appear because of rolling calculation)
    atr_data = atr_data.dropna()

    return atr_data

