#!/usr/bin/env python
# coding: utf-8

# In[44]:


import requests
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import QuantileTransformer
from datetime import datetime

# Function to fetch the list of BTC prices from the API
def fetch_btc_price_list():
    url = 'https://bitcoin-data.com/api/v1/btc-price'  # Replace with the actual API endpoint
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            return data
        else:
            print("Unexpected data format or empty list.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to fetch the MVRV Ratio from the API
def fetch_mvrv_ratio_list():
    url = 'https://bitcoin-data.com/api/v1/mvrv'  # Updated endpoint for MVRV Ratio
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            return data
        else:
            print("Unexpected data format or empty list.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def plot_btc_and_mvrv(data_btc, data_mvrv):
    # Truncate BTC data to start at 2012
    data_btc = [entry for entry in data_btc if datetime.strptime(entry['d'], '%Y-%m-%d').year >= 2012]

    # Extract dates and log-transformed prices for BTC
    dates_btc = [datetime.strptime(entry['d'], '%Y-%m-%d') for entry in data_btc]
    prices_btc = [np.log10(float(entry['btcPrice'])) for entry in data_btc]

    # Filter and extract dates and MVRV Ratio
    data_mvrv = [entry for entry in data_mvrv if entry['mvrv'] is not None]
    dates_mvrv = [datetime.strptime(entry['d'], '%Y-%m-%d') for entry in data_mvrv]
    mvrv_values = np.array([float(entry['mvrv']) for entry in data_mvrv]).reshape(-1, 1)

    # Quantile Normalization
    transformer = QuantileTransformer(output_distribution='uniform')
    mvrv_normalized = transformer.fit_transform(mvrv_values).flatten()

    # Define thresholds for overbought and oversold
    overbought_threshold = 0.975
    oversold_threshold = 0.025

    # Create the plot with dual y-axes
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plot vertical lines first to ensure they are at the back
    overbought_label_added = False
    oversold_label_added = False

    for date, value in zip(dates_mvrv, mvrv_normalized):
        if value > overbought_threshold:
            ax1.axvline(
                date, color='red', linestyle='-', linewidth=1,
                label='Overbought (Top 2.5%)' if not overbought_label_added else "", zorder=1
            )
            overbought_label_added = True
        elif value < oversold_threshold:
            ax1.axvline(
                date, color='green', linestyle='-', linewidth=1,
                label='Oversold (Bottom 2.5%)' if not oversold_label_added else "", zorder=1
            )
            oversold_label_added = True

    # Plot BTC price on the left y-axis
    ax1.set_xlabel('Date')
    ax1.set_ylabel('BTC Price (USD)', color='blue')
    ax1.plot(dates_btc, prices_btc, color='blue', label='BTC Price (USD)', zorder=2)
    ax1.tick_params(axis='y', labelcolor='blue')

    # Set y-ticks for BTC prices in powers of 10
    y_ticks = [1, 10, 100, 1000, 10000, 100000]
    ax1.set_yticks(np.log10(y_ticks))
    ax1.set_yticklabels(y_ticks)
    # Plot normalized MVRV Ratio on the secondary y-axis
    ax2 = ax1.twinx()
    ax2.set_ylabel('Normalized MVRV Ratio', color='orange')
    ax2.plot(dates_mvrv, mvrv_normalized, color='orange', label='Normalized MVRV Ratio', linestyle='-', zorder=3)
    ax2.tick_params(axis='y', labelcolor='orange')

    # Create the legend last to ensure it is on top
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    legend = ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', bbox_to_anchor=(0.01, 1))
    legend.set_zorder(5)  # Bring the legend to the front

    # Update the title
    fig.suptitle('Normalized MVRV')

    plt.grid(True)
    plt.show()

# Main execution
btc_price_list = fetch_btc_price_list()
mvrv_ratio_list = fetch_mvrv_ratio_list()

if btc_price_list is not None and mvrv_ratio_list is not None:
    plot_btc_and_mvrv(btc_price_list, mvrv_ratio_list)
else:
    print("Failed to fetch data for BTC price or MVRV Ratio.")




# In[ ]:




