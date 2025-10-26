# Pieter's Portfolio Tracker (CSV + Yahoo Finance)

A lightweight, command‑line portfolio tracker that reads your trades from a CSV file and pulls live data (price, dividends, day & month moves) from Yahoo Finance via `yfinance`.

> The banner currently prints **“Pieter’s Portfolio Tracker”** — feel free to change that string in `main()`.

---

##  Features

* Add stock purchases interactively and auto‑save to a CSV
* Aggregate holdings (total shares, average cost, fees)
* Live snapshot (current price/value, gain/loss, portfolio dividend yield)
* Performance: today’s change and last‑month change (value & %)
* Per‑holding breakdown with purchase history

---

##  Requirements

* Python 3.9+
* Packages: `pandas`, `yfinance`

```bash
pip install pandas yfinance
```

> **Note:** `yfinance` fetches market data from Yahoo Finance and can be rate‑limited. Prices may be delayed and sometimes fields (e.g., dividend info) are missing for certain tickers.

---

##  Quick Start

1. **Save the script** as `portfolio_tracker.py` (or keep your file name).
2. **Create a virtual env (optional but recommended):**

   ```bash
   python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. **Install deps:**

   ```bash
   pip install pandas yfinance
   ```
4. **Create an empty CSV** named `portfolio.csv` next to the script, with this header:

   ```csv
   symbol,purchase_date,purchase_price,quantity,fees
   ```

   Add your first line, for example:

   ```csv
   AAPL,2024-01-15,180.50,5,1.00
   ```
5. **Run:**

   ```bash
   python portfolio_tracker.py
   ```

---

##  CSV Format

The app reads and writes a single CSV (`portfolio.csv`) with columns:

| column           | type   | example      | notes                                                                                          |
| ---------------- | ------ | ------------ | ---------------------------------------------------------------------------------------------- |
| `symbol`         | string | `AAPL`       | Use Yahoo Finance tickers. For non‑US markets include the suffix (e.g., `NESN.SW`, `ASML.AS`). |
| `purchase_date`  | date   | `2024-01-15` | Format `YYYY-MM-DD`.                                                                           |
| `purchase_price` | float  | `180.50`     | Price per share in your base currency.                                                         |
| `quantity`       | float  | `5`          | Number of shares. Supports decimals.                                                           |
| `fees`           | float  | `1.00`       | Commission/fees for that trade.                                                                |

You can add many rows per ticker; the tracker aggregates them.

---

##  Using the App (Menu)

When you run the script, you’ll see:

```
Options:
1. Add stock purchase
2. View portfolio with performances
3. Save and exit
```

* **1. Add stock purchase** — prompts you for `symbol`, `date`, `price`, `quantity`, `fees`. Instantly saves back to `portfolio.csv`.
* **2. View portfolio with performances** — loads holdings, fetches live data (price, dividends, day & month changes) and prints a summary.
* **3. Save and exit** — writes the current in‑memory portfolio to CSV and quits.

> Live data is optional in the code: `display_portfolio(include_current_prices=True, include_performance=True)`

---

##  What the Summary Shows

* **Total Invested / Fees / Total Cost** — sums across all purchases
* **Current Value** — price × shares (for holdings where a price is available)
* **Total Gain/Loss** — absolute and percentage vs total cost
* **Expected Annual Dividends** — per‑share trailing dividend × total shares
* **Portfolio Dividend Yield** — expected annual dividends ÷ current value
* **Today’s & Monthly Change** — value and % (based on recent close data)

Per holding, you’ll also see:

* Total shares, average cost per share
* Current price/value, gain/loss, dividend yield & annual dividend per share
* Today’s and monthly changes (value & %), when available
* Full list of purchases for that ticker

---

##  Project Structure (simple)

```
.
├── portfolio_tracker.py   # this script (or your filename)
└── portfolio.csv          # your trades live here
```

---

##  Notes, Tips & Limitations

* **Ticker symbols:** International tickers often need a suffix (e.g., `.AS`, `.SW`, `.L`). Check Yahoo Finance for the exact symbol.
* **Data availability:** Some fields from `yfinance.Ticker(...).info` may be absent; the code falls back to recent `history()` when needed.
* **Delays & currency:** Quotes can be delayed. The script assumes your CSV prices and Yahoo quotes are in the same currency.
* **Dividends:** Uses trailing dividend metrics; forward yields may differ.
* **Performance windows:** “Today” uses the previous available close; “Monthly” compares first vs last close in the last month window from `history()`.

---

##  Customizing

* Change the CSV file name by editing the `PortfolioTracker('portfolio.csv')` line in `main()`.
* Adjust the banner text in `main()`.
* Turn off performance metrics: call `display_portfolio(include_current_prices=True, include_performance=False)`.
---
