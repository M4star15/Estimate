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

df["Safety Score"] = (
    df["Market Cap"] / df["Market Cap"].max() +  # Normalize Market Cap
    df["Cash Flow Score"] +  # Strong cash flow = safer
    (1 / (df["Debt-to-Equity Ratio"] + 1))*0.5  # Lower debt is safer
) / 3  # Normalize overall safety

# Weighted score
df["Middle Score"] = (
    df["Revenue Growth"] * 0.2 +
    df["EPS Score"] * 0.15 +  # Reduce EPS impact
    df["ROE Score"] * 0.2 +
    (1 / df["P/E Score"]) * 0.15 +  # Lower P/E is better
    (1 / df["Debt Score"]) * 0.05 +  # Penalize high debt more
    df["Cash Flow Score"] * 0.25
)
df["Final Score"] = df["Middle Score"] * df["Safety Score"]


# Sort
df_sorted_final = df.sort_values(by="Final Score", ascending=False)
print(df_sorted_final[["Stock Symbol", "Company Name", "Final Score"]].head(30))
df_sorted_middle = df.sort_values(by="Middle Score", ascending=False)
print(df_sorted_middle[["Stock Symbol", "Company Name", "Middle Score"]].head(30))

top30_growth = df_sorted_growth.head(30)
plt.figure(figsize=(20, 10))
plt.barh(top30_growth["Company Name"], top30_growth["Revenue Growth"], color="green")
plt.xlabel("Revenue Growth")
plt.ylabel("Company")
plt.title("Top 30 Fastest Growing Companies")
plt.gca().invert_yaxis()  # Highest at the top
plt.show()

top30_cash = df_sorted_cash.head(30)
plt.figure(figsize=(20, 10))
plt.barh(top30_cash["Company Name"], top30_cash["Free Cash Flow"], color="blue")
plt.xlabel("Free Cash Flow (in billions)")
plt.ylabel("Company")
plt.title("Top 30 Companies with Strong Cash Flow")
plt.gca().invert_yaxis()
plt.show()

top30_final = df_sorted_final.head(30)
plt.figure(figsize=(20, 10))
plt.barh(top30_final["Company Name"], top30_final["Final Score"], color="purple")
plt.xlabel("Final Investment Score")
plt.ylabel("Company")
plt.title("Top 30 Investment Opportunities")
plt.gca().invert_yaxis()
plt.show()

top30_middle = df_sorted_middle.head(30)
plt.figure(figsize=(20, 10))
plt.barh(top30_middle["Company Name"], top30_middle["Middle Score"], color="red")
plt.xlabel("Investment Score without risk factor")
plt.ylabel("Company")
plt.title("Top 30 Investment Opportunities without risk factor applied")
plt.gca().invert_yaxis()
plt.show()

growth_stocks = df[df["Revenue Growth"] > 0.2].sort_values(by="Revenue Growth", ascending=False)
print(growth_stocks.head(10))
value_stocks = df[(df["P/E Ratio"] < 15) & (df["Return on Equity (ROE)"] > 0.15)]
print(value_stocks.head(10))
safe_stocks = df[(df["Free Cash Flow"] > 1e9) & (df["Debt-to-Equity Ratio"] < 0.5)]
print(safe_stocks.head(10))
