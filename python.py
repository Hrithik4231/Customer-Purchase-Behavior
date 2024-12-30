# Import libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
file_path = "D:\\dataset\\customer_purchase_data.csv"  # Replace with your dataset file name
try:
    df = pd.read_csv(file_path)
    print("Dataset loaded successfully!")
    print("\nFirst 5 rows:")
    print(df.head())
except FileNotFoundError:
    print("Error: File not found. Check the file path and name.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()

# Normalize column names to lowercase for consistency
df.columns = df.columns.str.lower()
print("\nNormalized Column Names:")
print(df.columns)

# Check for null values
print("\nNull Values Summary:")
print(df.isnull().sum())

# Summary statistics
print("\nSummary Statistics:")
print(df.describe())

# Visualization 1: Distribution of a numeric column
plt.figure(figsize=(8, 6))
numeric_col = input("Enter a numeric column for distribution plot: ").lower()  # User input in lowercase
if numeric_col in df.columns and pd.api.types.is_numeric_dtype(df[numeric_col]):
    sns.histplot(df[numeric_col], kde=True, bins=10, color='blue')
    plt.title(f'Distribution of {numeric_col.capitalize()}')
    plt.xlabel(numeric_col.capitalize())
    plt.ylabel('Frequency')
    plt.show()
else:
    print(f"Error: Column '{numeric_col}' not found in the dataset or it is not numeric.")

# Visualization 2: Scatter Plot between two numeric columns
plt.figure(figsize=(8, 6))
x_col = input("Enter the column for X-axis: ").lower()
y_col = input("Enter the column for Y-axis: ").lower()
if x_col in df.columns and y_col in df.columns and pd.api.types.is_numeric_dtype(df[x_col]) and pd.api.types.is_numeric_dtype(df[y_col]):
    sns.scatterplot(x=df[x_col], y=df[y_col], palette='coolwarm', s=100)
    plt.title(f'{x_col.capitalize()} vs {y_col.capitalize()}')
    plt.xlabel(x_col.capitalize())
    plt.ylabel(y_col.capitalize())
    plt.show()
else:
    print(f"Error: Columns '{x_col}' or '{y_col}' not found in the dataset or are not numeric.")

# Visualization 3: Correlation Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='YlGnBu', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()

# Visualization 4: Box Plot for Categorical vs Numeric
plt.figure(figsize=(8, 6))
cat_col = input("Enter a categorical column for box plot: ").lower()
if cat_col in df.columns and pd.api.types.is_categorical_dtype(df[cat_col]) or df[cat_col].dtype == 'object':  # Check if the column is categorical
    if y_col in df.columns and pd.api.types.is_numeric_dtype(df[y_col]):
        sns.boxplot(x=df[cat_col], y=df[y_col], palette='viridis')
        plt.title(f'{y_col.capitalize()} by {cat_col.capitalize()}')
        plt.xlabel(cat_col.capitalize())
        plt.ylabel(y_col.capitalize())
        plt.show()
    else:
        print(f"Error: '{y_col}' is not a numeric column for the box plot.")
else:
    print(f"Error: Column '{cat_col}' not found in the dataset or it is not categorical.")
