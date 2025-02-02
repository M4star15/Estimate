import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

df = pd.read_csv("all_stock_data.csv")

df.dropna(inplace=True)

df["Revenue Growth"] = pd.to_numeric(df["Revenue Growth"], errors="coerce")
df["EPS"] = pd.to_numeric(df["EPS"], errors="coerce")
df["P/E Ratio"] = pd.to_numeric(df["P/E Ratio"], errors="coerce")
df["Return on Equity (ROE)"] = pd.to_numeric(df["Return on Equity (ROE)"], errors="coerce")
df["Debt-to-Equity Ratio"] = pd.to_numeric(df["Debt-to-Equity Ratio"], errors="coerce")
df["Free Cash Flow"] = pd.to_numeric(df["Free Cash Flow"], errors="coerce")


print(df.info())  



from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Select relevant features for clustering
features = ["Revenue Growth", "EPS", "P/E Ratio", "Return on Equity (ROE)", "Debt-to-Equity Ratio", "Free Cash Flow"]
df[features] = df[features].replace([np.inf, -np.inf], np.nan)  # Convert infinite to NaN
df.dropna(subset=features, inplace=True)  # Remove rows with missing values
#df[features] = df[features].fillna(df[features].median())

df_scaled = df.copy()
df_scaled[features] = StandardScaler().fit_transform(df_scaled[features])
print(df_scaled[features].describe())


# Apply K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df_scaled["Cluster"] = kmeans.fit_predict(df_scaled[features])

# Visualize Clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df_scaled["P/E Ratio"], y=df_scaled["EPS"], hue=df_scaled["Cluster"], palette="viridis")
plt.title("Stock Clusters Based on Financial Metrics")
plt.xlabel("P/E Ratio")
plt.ylabel("EPS")
plt.show()


# Define independent variables (features) and dependent variable (target)
X = df[["Revenue Growth", "EPS", "P/E Ratio", "Return on Equity (ROE)", "Debt-to-Equity Ratio", "Free Cash Flow"]]
y = df["Latest Close Price"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Evaluate model performance
print("R-squared score:", r2_score(y_test, y_pred))


# Compute Z-Scores for P/E Ratio (Identifying Overvalued Stocks)
df["P/E Ratio"] = df["P/E Ratio"].replace([np.inf, -np.inf], np.nan)
df["P/E Z-Score"] = zscore(df["P/E Ratio"])

# Find extreme values (above 2.5 or below -2.5)
outliers = df[(df["P/E Z-Score"] > 2.5) | (df["P/E Z-Score"] < -2.5)]
print(outliers[["Stock Symbol", "Company Name", "P/E Ratio", "P/E Z-Score"]])

import numpy as np
import matplotlib.pyplot as plt

# Replace infinite values with NaN
df["Latest Close Price"] = df["Latest Close Price"].replace([np.inf, -np.inf], np.nan)

# Fill NaN values with median
df["Latest Close Price"].fillna(df["Latest Close Price"].median(), inplace=True)

# Check standard deviation (must not be 0 or NaN)
volatility = df["Latest Close Price"].std()
if np.isnan(volatility) or volatility == 0:
    volatility = 0.01  # Assign small positive value to avoid division errors

# Define number of trading days (change this if needed)
days = 252  # Standard stock market assumption
# days = 365  # If you want full year simulation

# Compute stock price safely
stock_price = df["Latest Close Price"].mean()

print(f"Stock Price Mean: {stock_price}")
print(f"Volatility (std): {volatility}")
print(f"Days Simulated: {days}")

# Run Monte Carlo Simulation safely
# Define parameters
simulations = 1000
days = int(days)  # Ensure it's an integer
simulated_prices = []

for _ in range(simulations):
    daily_returns = np.random.normal(0, volatility, int(days))
    price_series = [stock_price]

    for r in daily_returns:
        new_price = price_series[-1] * (1 + r)

        # Prevent infinite or negative values
        if new_price > 1e9:  # Set upper limit
            new_price = 1e9
        elif new_price < 1e-3:  # Set lower limit
            new_price = 1e-3

        price_series.append(new_price)

    simulated_prices.append(price_series)


# Convert safely
simulated_prices = np.array(simulated_prices)


# Check for errors before plotting
if np.isnan(simulated_prices).any():
    print("Error: Monte Carlo simulation contains NaN values!")
    
else:
    
    plt.figure(figsize=(12, 6))
    plt.plot(simulated_prices.T, color="gray", alpha=0.1)
    plt.title("Monte Carlo Simulation of Stock Prices (Next 1 Year)")
    plt.xlabel("Days")
    plt.ylabel("Stock Price")
    plt.show()
