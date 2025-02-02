import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("all_stock_data.csv")
print(df.head())
print(df.isnull().sum())
df_sorted_growth = df.sort_values(by="Revenue Growth", ascending=False)
print(df_sorted_growth[["Stock Symbol", "Company Name", "Revenue Growth"]].head(10))
df_sorted_eps = df.sort_values(by="EPS", ascending=False)
print(df_sorted_eps[["Stock Symbol", "Company Name", "EPS"]].head(10))

df_sorted_roe = df.sort_values(by="Return on Equity (ROE)", ascending=False)
print(df_sorted_roe[["Stock Symbol", "Company Name", "Return on Equity (ROE)"]].head(10))
df_sorted_pe = df.sort_values(by="P/E Ratio", ascending=True)
print(df_sorted_pe[["Stock Symbol", "Company Name", "P/E Ratio"]].head(10))
df_sorted_debt = df.sort_values(by="Debt-to-Equity Ratio", ascending=False)
print(df_sorted_debt[["Stock Symbol", "Company Name", "Debt-to-Equity Ratio"]].head(10))
df_sorted_cash = df.sort_values(by="Free Cash Flow", ascending=False)
print(df_sorted_cash[["Stock Symbol", "Company Name", "Free Cash Flow"]].head(10))

# Normalize each metric
df["Revenue Growth Score"] = df["Revenue Growth"] / df["Revenue Growth"].max()
df["EPS Score"] = df["EPS"] / df["EPS"].max()
df["ROE Score"] = df["Return on Equity (ROE)"] / df["Return on Equity (ROE)"].max()
df["P/E Score"] = 1 / df["P/E Ratio"]  # Lower is better
df["Debt Score"] = 1 / (df["Debt-to-Equity Ratio"] + 1)  # Lower debt is better
df["Cash Flow Score"] = df["Free Cash Flow"] / df["Free Cash Flow"].max()

# Weighted score
df["Final Score"] = (
    df["Revenue Growth Score"] * 0.2 +
    df["EPS Score"] * 0.2 +
    df["ROE Score"] * 0.2 +
    df["P/E Score"] * 0.15 +
    df["Debt Score"] * 0.15 +
    df["Cash Flow Score"] * 0.1
)

# Sort
df_sorted_final = df.sort_values(by="Final Score", ascending=False)
print(df_sorted_final[["Stock Symbol", "Company Name", "Final Score"]].head(10))

top10_growth = df_sorted_growth.head(10)
plt.figure(figsize=(12, 6))
plt.barh(top10_growth["Company Name"], top10_growth["Revenue Growth"], color="green")
plt.xlabel("Revenue Growth")
plt.ylabel("Company")
plt.title("Top 10 Fastest Growing Companies")
plt.gca().invert_yaxis()  # Highest at the top
plt.show()

top10_cash = df_sorted_cash.head(10)
plt.figure(figsize=(12, 6))
plt.barh(top10_cash["Company Name"], top10_cash["Free Cash Flow"], color="blue")
plt.xlabel("Free Cash Flow (in billions)")
plt.ylabel("Company")
plt.title("Top 10 Companies with Strong Cash Flow")
plt.gca().invert_yaxis()
plt.show()

top100_final = df_sorted_final.head(100)
plt.figure(figsize=(102, 60))
plt.barh(top100_final["Company Name"], top100_final["Final Score"], color="purple")
plt.xlabel("Final Investment Score")
plt.ylabel("Company")
plt.title("Top 100 Investment Opportunities")
plt.gca().invert_yaxis()
plt.show()

growth_stocks = df[df["Revenue Growth"] > 0.2].sort_values(by="Revenue Growth", ascending=False)
print(growth_stocks.head(10))
value_stocks = df[(df["P/E Ratio"] < 15) & (df["Return on Equity (ROE)"] > 0.15)]
print(value_stocks.head(10))
safe_stocks = df[(df["Free Cash Flow"] > 1e9) & (df["Debt-to-Equity Ratio"] < 0.5)]
print(safe_stocks.head(10))
