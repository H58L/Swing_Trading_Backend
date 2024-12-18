import pandas as pd

def calculate_fibonacci_retracement(stock_data):
    """
    Calculates Fibonacci retracement levels based on the highest and lowest prices in the dataset.

    Args:
        stock_data (pd.DataFrame): Dataframe containing stock price data with 'High', 'Low', 'Close', and 'Date' columns.

    Returns:
        dict: A dictionary containing Fibonacci retracement levels and the stock data.
    """
    # Ensure required columns exist
    required_columns = {"High", "Low", "Close", "Date"}
    if not required_columns.issubset(stock_data.columns):
        raise ValueError(f"Missing required columns. Ensure {required_columns} are present in the data.")

    # Calculate the highest and lowest price
    highest_price = stock_data["High"].max()
    lowest_price = stock_data["Low"].min()
    diff = highest_price - lowest_price

    # Calculate Fibonacci levels
    levels = {
        "100% (High)": round(highest_price, 2),
        "76.4%": round(highest_price - 0.236 * diff, 2),
        "61.8%": round(highest_price - 0.382 * diff, 2),
        "50.0%": round(highest_price - 0.5 * diff, 2),
        "38.2%": round(highest_price - 0.618 * diff, 2),
        "23.6%": round(highest_price - 0.764 * diff, 2),
        "0% (Low)": round(lowest_price, 2),
    }

    # Format stock data: Ensure only 'Date' and 'Close' are included
    stock_data = stock_data[['Date', 'Close']].copy()
    stock_data['Date'] = pd.to_datetime(stock_data['Date']).dt.strftime('%Y-%m-%d')  # Format dates to string

    # Convert the stock data into a list of dictionaries
    stock_data_list = stock_data.to_dict(orient="records")

    # Final output
    result = {
        "fibonacci_levels": levels,
        "stock_data": stock_data_list
    }

    return result

