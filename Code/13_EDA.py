import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("../Data/Processed/07_weather_data_integrated.csv")
df2 = pd.read_csv("../Data/Processed/05_Human_Readable.csv")

print(df.head())  # first 5 rows
print("############################################################################")
print(df.info())  # data types, non‑null counts
print("############################################################################")
print(df.describe(include="all"))  # extended stats for all columns
print("############################################################################")
print(df2.describe(include="all"))

# Number of People Histogram
sns.histplot(data=df, x="Number of People", kde=True)
plt.title("Distribution of Target")
plt.show()

# Number of People Boxplot
sns.boxplot(x=df["Number of People"])
plt.title("Boxplot of Target")
plt.show()

# Number of Vehicles Histogram
sns.histplot(data=df, x="Number of Road Vehicles", kde=True)
plt.title("Distribution of Target")
plt.show()

# Number of Vehicles Boxplot
sns.boxplot(data=df, x="Number of Road Vehicles")
plt.title("Boxplot of Target")
plt.show()

# Number of Bicycles Histogram
sns.histplot(data=df, x="Number of Bicycles", kde=True)
plt.title("Distribution of Target")
plt.show()

# Number of Bicycles Boxplot
sns.boxplot(x=df["Number of Bicycles"])
plt.title("Boxplot of Target")
plt.show()
