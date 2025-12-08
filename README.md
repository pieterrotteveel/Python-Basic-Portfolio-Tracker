# Python Basic Portfolio Tracker with Yahoo Finance Integration

A simple Python application to track your stock portfolio from CSV data with real-time price updates and dividend tracking from Yahoo Finance.

## Features

- Load stock purchases from CSV file
- Track purchase date, price, quantity, and fees
- Calculate portfolio statistics (total invested, fees, average cost per share)
- **Real-time price updates from Yahoo Finance**
- **Calculate current portfolio value and gains/losses**
- **Dividend yield tracking and annual dividend calculations**
- Interactive command-line interface
- Save portfolio data back to CSV

## CSV File Format

Your CSV file should have the following columns:
- `symbol`: Stock symbol (e.g., AAPL, MSFT)
- `purchase_date`: Date in YYYY-MM-DD format
- `purchase_price`: Price per share at purchase
- `quantity`: Number of shares purchased
- `fees`: Transaction fees

Example:
```csv
symbol,purchase_date,purchase_price,quantity,fees
AAPL,2024-01-15,180.50,10,9.99
MSFT,2024-02-20,350.25,5,9.99
```

## Usage

1. Run the portfolio tracker:
```bash
python portfolio_tracker.py
```

2. The program will look for `portfolio.csv` by default. If it doesn't exist, you can start with an empty portfolio.

3. Use the interactive menu to:
   - Add new stock purchases
   - View your portfolio summary (basic view)
   - **View portfolio with current prices, gains/losses, and dividend information**
   - Save and exit

## Yahoo Finance Features

- **Option 3**: View portfolio with current prices fetches real-time data from Yahoo Finance
- Shows current stock prices, portfolio value, and gain/loss calculations
- **Displays dividend yields for each stock**
- **Calculates expected annual dividends for individual holdings and total portfolio**
- **Shows portfolio-wide dividend yield**
- Displays both dollar amounts and percentage gains/losses
- Works with most stock symbols available on Yahoo Finance

## Example Output

The portfolio tracker will show:
- Total amount invested and fees paid
- **Current portfolio value (when using price updates)**
- **Total and individual stock gains/losses**
- **Expected annual dividends and dividend yields**
- **Portfolio dividend yield percentage**
- Number of different holdings
- Breakdown by stock symbol with average cost per share
- Individual purchase history

## Requirements

- Python 3.6+
- pandas library
- **yfinance library** (for Yahoo Finance integration)

Install dependencies:
```bash
pip install pandas yfinance
```

## Notes

- Current price and dividend fetching requires an internet connection
- Yahoo Finance data may have slight delays
- Dividend information is based on current/trailing annual dividend rates
- Some symbols might not be available or may require different formatting
- Stocks that don't pay dividends will show 0% dividend yield