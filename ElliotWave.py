import yfinance as yf
# from scipy.signal import find_peaks
import pandas as pd
import numpy as np



def find_peaks(data, distance):
    peaks = []
    for i in range(1, len(data) - 1):
        if data[i] > data[i - 1] and data[i] > data[i + 1] and data[i] > distance:
            peaks.append(i)
    return peaks


# def calculate_elliott_wave(data):
#     # Ensure the data has a 'Close' column and drop any NaN values
#     prices = data['Close'].dropna().values
#     dates = data['Date']  # Using the 'Date' column after reset_index

#     # Find peaks (local maxima)
#     peaks, _ = find_peaks(prices, 5)

#     # Find troughs (local minima by inverting the data)
#     troughs, _ = find_peaks(-prices, distance=5)

#     return peaks, troughs, prices, dates

def calculate_elliott_wave(data):
    # Ensure the data has a 'Close' column and drop any NaN values
    prices = data['Close'].dropna().values
    dates = data['Date']  # Using the 'Date' column after reset_index

    # Find peaks (local maxima)
    peaks = find_peaks(prices, 5)  # Custom find_peaks returns only peaks

    # Find troughs (local minima by inverting the data)
    troughs = find_peaks(-prices, 5)  # No unpacking, just use the returned value

    return peaks, troughs, prices, dates


def identify_buy_sell_signals(peaks, troughs, prices, dates):
    # Convert dates to string format for JSON serialization
    buy_signals = [(dates[trough].strftime("%Y-%m-%d"), prices[trough]) for trough in troughs]
    sell_signals = [(dates[peak].strftime("%Y-%m-%d"), prices[peak]) for peak in peaks]
    return buy_signals, sell_signals

