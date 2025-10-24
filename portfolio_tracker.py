import csv
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict

class PortfolioTracker:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.portfolio_data = []
        self.load_portfolio()
    
    def load_portfolio(self):
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                self.portfolio_data = list(reader)
                for row in self.portfolio_data:
                    row['quantity'] = float(row['quantity'])
                    row['purchase_price'] = float(row['purchase_price'])
                    row['fees'] = float(row['fees'])
                    row['purchase_date'] = datetime.strptime(row['purchase_date'], '%Y-%m-%d')
        except FileNotFoundError:
            print(f"CSV file '{self.csv_file}' not found. Starting with empty portfolio.")
            self.portfolio_data = []
        except Exception as e:
            print(f"Error loading portfolio: {e}")
            self.portfolio_data = []
    
    def get_current_price(self, symbol: str) -> float:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            if current_price is None:
                hist = ticker.history(period="1d")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
            return float(current_price) if current_price else None
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None
    
    def get_dividend_yield(self, symbol: str) -> float:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            dividend_yield = info.get('dividendYield')
            if dividend_yield is not None:
                return float(dividend_yield) * 100
            else:
                trailing_yield = info.get('trailingAnnualDividendYield')
                if trailing_yield is not None:
                    return float(trailing_yield) * 100
            return 0.0
        except Exception as e:
            print(f"Error fetching dividend yield for {symbol}: {e}")
            return None
    
    def get_stock_info(self, symbol: str) -> Dict:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            if current_price is None:
                hist = ticker.history(period="1d")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
            
            dividend_yield = info.get('dividendYield') or info.get('trailingAnnualDividendYield') or 0
            if dividend_yield:
                dividend_yield = float(dividend_yield) * 100 
            
            annual_dividend = info.get('trailingAnnualDividendRate') or 0
            
            return {
                'current_price': float(current_price) if current_price else None,
                'dividend_yield': float(dividend_yield),
                'annual_dividend': float(annual_dividend) if annual_dividend else 0
            }
        except Exception as e:
            print(f"Error fetching stock info for {symbol}: {e}")
            return {
                'current_price': None,
                'dividend_yield': 0.0,
                'annual_dividend': 0.0
            }
    
    def get_current_prices(self, symbols: List[str]) -> Dict[str, float]:
        prices = {}
        for symbol in symbols:
            price = self.get_current_price(symbol)
            if price:
                prices[symbol] = price
        return prices

    def get_stock_info_bulk(self, symbols: List[str]) -> Dict[str, Dict]:
        stock_info = {}
        for symbol in symbols:
            stock_info[symbol] = self.get_stock_info(symbol)
        return stock_info
    
    def add_stock(self, symbol: str, purchase_date: str, purchase_price: float, 
                  quantity: float, fees: float = 0.0):
        stock_entry = {
            'symbol': symbol.upper(),
            'purchase_date': datetime.strptime(purchase_date, '%Y-%m-%d'),
            'purchase_price': purchase_price,
            'quantity': quantity,
            'fees': fees
        }
        self.portfolio_data.append(stock_entry)
        print(f"Added {quantity} shares of {symbol} purchased on {purchase_date}")

        self.save_portfolio()
        print(f"Stock automatically saved to {self.csv_file}")
    
    def save_portfolio(self):
        try:
            with open(self.csv_file, 'w', newline='') as file:
                fieldnames = ['symbol', 'purchase_date', 'purchase_price', 'quantity', 'fees']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in self.portfolio_data:
                    row_copy = row.copy()
                    row_copy['purchase_date'] = row['purchase_date'].strftime('%Y-%m-%d')
                    writer.writerow(row_copy)
            print(f"Portfolio saved to {self.csv_file}")
        except Exception as e:
            print(f"Error saving portfolio: {e}")
    
    def get_historical_prices(self, symbol: str, period: str = "1mo") -> Dict:
        """Get historical prices for performance calculations"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return {'current': None, 'previous': None}
            
            current_price = hist['Close'].iloc[-1]
            
            if period in ["1d", "2d", "5d"] and len(hist) >= 2:
                previous_price = hist['Close'].iloc[-2]
            elif period == "1mo" and len(hist) >= 2:
                previous_price = hist['Close'].iloc[0]
            else:
                previous_price = current_price
            
            return {
                'current': float(current_price),
                'previous': float(previous_price)
            }
        except Exception as e:
            print(f"Error fetching historical prices for {symbol}: {e}")
            return {'current': None, 'previous': None}
    
    def get_stock_info_with_performance(self, symbol: str) -> Dict:
        """Enhanced stock info with today's and monthly performance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            if current_price is None:
                hist = ticker.history(period="1d")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
            
            dividend_yield = info.get('dividendYield') or info.get('trailingAnnualDividendYield') or 0
            if dividend_yield:
                dividend_yield = float(dividend_yield) * 100 
            
            annual_dividend = info.get('trailingAnnualDividendRate') or 0
            

            daily_data = self.get_historical_prices(symbol, "5d")
            monthly_data = self.get_historical_prices(symbol, "1mo")
            

            today_change = 0.0
            today_change_percent = 0.0
            if daily_data['current'] and daily_data['previous'] and daily_data['current'] != daily_data['previous']:
                today_change = daily_data['current'] - daily_data['previous']
                today_change_percent = (today_change / daily_data['previous']) * 100
            
            monthly_change = 0.0
            monthly_change_percent = 0.0
            if monthly_data['current'] and monthly_data['previous'] and monthly_data['current'] != monthly_data['previous']:
                monthly_change = monthly_data['current'] - monthly_data['previous']
                monthly_change_percent = (monthly_change / monthly_data['previous']) * 100
            
            return {
                'current_price': float(current_price) if current_price else None,
                'dividend_yield': float(dividend_yield),
                'annual_dividend': float(annual_dividend) if annual_dividend else 0,
                'today_change': today_change,
                'today_change_percent': today_change_percent,
                'monthly_change': monthly_change,
                'monthly_change_percent': monthly_change_percent
            }
        except Exception as e:
            print(f"Error fetching stock info with performance for {symbol}: {e}")
            return {
                'current_price': None,
                'dividend_yield': 0.0,
                'annual_dividend': 0.0,
                'today_change': 0.0,
                'today_change_percent': 0.0,
                'monthly_change': 0.0,
                'monthly_change_percent': 0.0
            }

    def get_stock_info_bulk_with_performance(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get stock info with performance for multiple symbols"""
        stock_info = {}
        for symbol in symbols:
            stock_info[symbol] = self.get_stock_info_with_performance(symbol)
        return stock_info
    
    def get_portfolio_summary(self, include_current_prices: bool = False, include_performance: bool = False) -> Dict:
        if not self.portfolio_data:
            return {"message": "Portfolio is empty"}
        
        summary = {}
        total_invested = 0
        total_fees = 0
        
        holdings = {}
        symbols = []
        
        for entry in self.portfolio_data:
            symbol = entry['symbol']
            if symbol not in holdings:
                holdings[symbol] = {
                    'total_shares': 0,
                    'total_cost': 0,
                    'total_fees': 0,
                    'purchases': []
                }
                symbols.append(symbol)
            
            cost = entry['purchase_price'] * entry['quantity']
            holdings[symbol]['total_shares'] += entry['quantity']
            holdings[symbol]['total_cost'] += cost
            holdings[symbol]['total_fees'] += entry['fees']
            holdings[symbol]['purchases'].append({
                'date': entry['purchase_date'].strftime('%Y-%m-%d'),
                'price': entry['purchase_price'],
                'quantity': entry['quantity'],
                'fees': entry['fees']
            })
            
            total_invested += cost
            total_fees += entry['fees']
        
        for symbol, data in holdings.items():
            data['avg_cost_per_share'] = data['total_cost'] / data['total_shares']
        
        total_current_value = 0
        total_gain_loss = 0
        total_annual_dividends = 0
        total_today_change = 0
        total_monthly_change = 0
        
        if include_current_prices or include_performance:
            if include_performance:
                print("Fetching current prices, dividend data, and performance metrics from Yahoo Finance...")
                stock_info = self.get_stock_info_bulk_with_performance(symbols)
            else:
                print("Fetching current prices and dividend data from Yahoo Finance...")
                stock_info = self.get_stock_info_bulk(symbols)
            
            for symbol, data in holdings.items():
                if symbol in stock_info and stock_info[symbol]['current_price']:
                    info = stock_info[symbol]
                    current_price = info['current_price']
                    dividend_yield = info['dividend_yield']
                    annual_dividend_per_share = info['annual_dividend']
                    
                    current_value = current_price * data['total_shares']
                    gain_loss = current_value - data['total_cost']
                    gain_loss_percent = (gain_loss / data['total_cost']) * 100
                    
                    expected_annual_dividends = annual_dividend_per_share * data['total_shares']
                    
                    data['current_price'] = current_price
                    data['current_value'] = current_value
                    data['gain_loss'] = gain_loss
                    data['gain_loss_percent'] = gain_loss_percent
                    data['dividend_yield'] = dividend_yield
                    data['annual_dividend_per_share'] = annual_dividend_per_share
                    data['expected_annual_dividends'] = expected_annual_dividends
                    
                    total_current_value += current_value
                    total_gain_loss += gain_loss
                    total_annual_dividends += expected_annual_dividends
                    
                    if include_performance and 'today_change' in info:
                        today_value_change = info['today_change'] * data['total_shares']
                        monthly_value_change = info['monthly_change'] * data['total_shares']
                        
                        data['today_change'] = info['today_change']
                        data['today_change_percent'] = info['today_change_percent']
                        data['today_value_change'] = today_value_change
                        data['monthly_change'] = info['monthly_change']
                        data['monthly_change_percent'] = info['monthly_change_percent']
                        data['monthly_value_change'] = monthly_value_change
                        
                        total_today_change += today_value_change
                        total_monthly_change += monthly_value_change
        
        summary = {
            'total_invested': round(total_invested, 2),
            'total_fees': round(total_fees, 2),
            'total_with_fees': round(total_invested + total_fees, 2),
            'number_of_holdings': len(holdings),
            'holdings': holdings
        }
        
        if (include_current_prices or include_performance) and total_current_value > 0:
            total_gain_loss_percent = (total_gain_loss / total_invested) * 100
            portfolio_dividend_yield = (total_annual_dividends / total_current_value) * 100 if total_current_value > 0 else 0
            
            summary['total_current_value'] = round(total_current_value, 2)
            summary['total_gain_loss'] = round(total_gain_loss, 2)
            summary['total_gain_loss_percent'] = round(total_gain_loss_percent, 2)
            summary['total_annual_dividends'] = round(total_annual_dividends, 2)
            summary['portfolio_dividend_yield'] = round(portfolio_dividend_yield, 2)

            if include_performance:
                today_change_percent = (total_today_change / (total_current_value - total_today_change)) * 100 if (total_current_value - total_today_change) > 0 else 0
                monthly_change_percent = (total_monthly_change / (total_current_value - total_monthly_change)) * 100 if (total_current_value - total_monthly_change) > 0 else 0
                
                summary['total_today_change'] = round(total_today_change, 2)
                summary['total_today_change_percent'] = round(today_change_percent, 2)
                summary['total_monthly_change'] = round(total_monthly_change, 2)
                summary['total_monthly_change_percent'] = round(monthly_change_percent, 2)
        
        return summary
    
    def display_portfolio(self, include_current_prices: bool = False, include_performance: bool = False):
        summary = self.get_portfolio_summary(include_current_prices, include_performance)
        
        if "message" in summary:
            print(summary["message"])
            return
        
        print("\n" + "="*70)
        print("PORTFOLIO SUMMARY")
        print("="*70)
        print(f"Total Invested: ${summary['total_invested']:,.2f}")
        print(f"Total Fees: ${summary['total_fees']:,.2f}")
        print(f"Total Cost: ${summary['total_with_fees']:,.2f}")
        
        if (include_current_prices or include_performance) and 'total_current_value' in summary:
            print(f"Current Value: ${summary['total_current_value']:,.2f}")
            gain_loss_color = "+" if summary['total_gain_loss'] >= 0 else ""
            print(f"Total Gain/Loss: {gain_loss_color}${summary['total_gain_loss']:,.2f} ({summary['total_gain_loss_percent']:+.2f}%)")
            
            if include_performance and 'total_today_change' in summary:
                today_color = "+" if summary['total_today_change'] >= 0 else ""
                monthly_color = "+" if summary['total_monthly_change'] >= 0 else ""
                print(f"Today's Change: {today_color}${summary['total_today_change']:,.2f} ({summary['total_today_change_percent']:+.2f}%)")
                print(f"Monthly Change: {monthly_color}${summary['total_monthly_change']:,.2f} ({summary['total_monthly_change_percent']:+.2f}%)")
            
            print(f"Expected Annual Dividends: ${summary['total_annual_dividends']:,.2f}")
            print(f"Portfolio Dividend Yield: {summary['portfolio_dividend_yield']:.2f}%")
        
        print(f"Number of Holdings: {summary['number_of_holdings']}")
        
        print("\n" + "="*70)
        print("HOLDINGS BREAKDOWN")
        print("="*70)
        
        for symbol, data in summary['holdings'].items():
            print(f"\n{symbol}:")
            print(f"  Total Shares: {data['total_shares']:,.2f}")
            print(f"  Average Cost per Share: ${data['avg_cost_per_share']:,.2f}")
            print(f"  Total Investment: ${data['total_cost']:,.2f}")
            print(f"  Total Fees: ${data['total_fees']:,.2f}")
            
            if (include_current_prices or include_performance) and 'current_price' in data:
                print(f"  Current Price: ${data['current_price']:,.2f}")
                print(f"  Current Value: ${data['current_value']:,.2f}")
                gain_loss_color = "+" if data['gain_loss'] >= 0 else ""
                print(f"  Gain/Loss: {gain_loss_color}${data['gain_loss']:,.2f} ({data['gain_loss_percent']:+.2f}%)")
                
                if include_performance and 'today_change' in data:
                    today_color = "+" if data['today_change'] >= 0 else ""
                    monthly_color = "+" if data['monthly_change'] >= 0 else ""
                    print(f"  Today's Change: {today_color}${data['today_change']:,.2f} ({data['today_change_percent']:+.2f}%) = {today_color}${data['today_value_change']:,.2f}")
                    print(f"  Monthly Change: {monthly_color}${data['monthly_change']:,.2f} ({data['monthly_change_percent']:+.2f}%) = {monthly_color}${data['monthly_value_change']:,.2f}")
                
                print(f"  Dividend Yield: {data['dividend_yield']:.2f}%")
                if data['expected_annual_dividends'] > 0:
                    print(f"  Expected Annual Dividends: ${data['expected_annual_dividends']:,.2f}")
                    print(f"  Annual Dividend per Share: ${data['annual_dividend_per_share']:.2f}")
            
            print(f"  Purchases:")
            for purchase in data['purchases']:
                print(f"    {purchase['date']}: {purchase['quantity']} shares @ ${purchase['price']:,.2f} (fees: ${purchase['fees']:,.2f})")

def main():
    print("======================================================")
    print("Pieter's Portfolio Tracker with Yahoo Finance Integration")
    print("======================================================")
    
    tracker = PortfolioTracker('portfolio.csv')
     
    while True:
        print("\nOptions:")
        print("1. Add stock purchase")
        print("2. View portfolio with performances")
        print("3. Save and exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            try:
                symbol = input("Enter stock symbol: ").strip().upper()
                date = input("Enter purchase date (YYYY-MM-DD): ").strip()
                price = float(input("Enter purchase price per share: $").strip())
                quantity = float(input("Enter quantity: ").strip())
                fees = float(input("Enter fees (or 0): $").strip() or "0")
                
                tracker.add_stock(symbol, date, price, quantity, fees)
            except ValueError:
                print("Invalid input. Please enter valid numbers for price, quantity, and fees.")
            except Exception as e:
                print(f"Error adding stock: {e}")
        
        elif choice == '2':
            tracker.display_portfolio(include_current_prices=True, include_performance=True)
        
        elif choice == '3':
            tracker.save_portfolio()
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
  

if __name__ == "__main__":
    main()
    