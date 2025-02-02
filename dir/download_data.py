import yfinance as yf
import pandas as pd
import time

# US Stock 
sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
sp500_table = pd.read_html(sp500_url)[0]  
stock_symbols = sp500_table["Symbol"].tolist() 
all_data = []
for stock in stock_symbols:
    try:
        ticker = yf.Ticker(stock)
        hist_data = ticker.history(period="5y")  # 5 years of data

        financials = ticker.info
        stock_data = {
            "Stock Symbol": stock,
            "Company Name": financials.get("longName"),
            "Industry": financials.get("industry"),
            "Market Cap": financials.get("marketCap"),
            "Revenue Growth": financials.get("revenueGrowth"),
            "EPS": financials.get("trailingEps"),
            "P/E Ratio": financials.get("trailingPE"),
            "Return on Equity (ROE)": financials.get("returnOnEquity"),
            "Debt-to-Equity Ratio": financials.get("debtToEquity"),
            "Operating Cash Flow": financials.get("operatingCashflow"),
            "Free Cash Flow": financials.get("freeCashflow"),
            "Latest Close Price": hist_data["Close"].iloc[-1] if not hist_data.empty else None,
        }
        all_data.append(stock_data)
        print(f"Fetched data for {stock}")

        time.sleep(1)  # Prevent rate limiting

    except Exception as e:
        print(f"Error fetching data for {stock}: {e}")

df = pd.DataFrame(all_data)
df.to_csv("all_stock_data.csv", index=False)
