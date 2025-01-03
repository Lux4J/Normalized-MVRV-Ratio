# Normalized MVRV Script

This script takes the MVRV Ratio for BTC and applies Quantile normalization in order to better quanitfy overbought and oversold zones, when the ratio is 2 standard deviations of the mean.

### How does it work?
The MVRV Ratio is calculated as: Market Cap/Realized Cap

The Marketcap is the total worth of all BTC in circulation. This is the number of coins(21,000,000) * the value of BTC at the current time.

The Realized Cap is the total worth of all BTC that it was acquired at. This is the number of coins(21,000,000) * the value that each BTC was purchased.

The idea of the MVRV Ratio is that:
* Rapid price appreciation will encourage sellers in profit to realize those gains. This is particularly pertinent when price has increased at such a rapid rate that nearly 100% of market participants are in profit.
* Price oscillates from periods of overbough and oversold with respective to the "true mean". This is the concept of reflexivity, as price increases, psychologically, the asset is percieved to be more valuable.
This causes price to overshoot to the upside and vice-versa to the downside. The MVRV is a simple metric that shows when price has appreciated to an unsustainable magnitude that a reversion is necessary.

The script applies qunatile normalization, a normalization technique. In short it takes the original distribution and maps it to a normal distribution while maintaining the 
original order of the data.

Overbought and oversold zones are marked when the Z > Score is + or - 1.96 respectively.

Below is the result of applying this to previous price data on BTC:

![image](https://github.com/user-attachments/assets/a7145f7e-c3af-43c6-a19c-f067eb72619e)

## Installation and Setup Instructions

### Prerequisites
Ensure you have Python (version 3.8 or later) installed on your system. You can download Python from the [official Python website](https://www.python.org/downloads/).

### Steps

1. **Clone or Download the Repository**
   - Clone the repository using Git:
     ```bash
     git clone https://github.com/Lux4J/Normalized-MVRV-Ratio.git
     cd Normalized_MVRV_Ratio
     ```
   - Or download the repository as a ZIP file, extract it, and navigate to the folder.

2. **Install Required Libraries**
   Type the following command to install the required libraries:
   ```bash
   pip install pandas numpy matplotlib
   ```

3. **Run the script**
To run the script type the following command in the terminal:
```
python Normalized_MVRV.py
```
