import pandas as pd;

def analyze_df(filename):
    df = pd.read_csv(f'data/raw/{filename}')
    print(f"\n=== {filename} ===")
    print("Shape:", df.shape)
    print("\nColumns:", df.columns.tolist())
    print("\nMissing values:\n", df.isnull().sum())
    print("\nSample data:\n", df.head(2))
    return df

files = [
    'olist_customers_dataset.csv',
    'olist_orders_dataset.csv',
    'olist_order_items_dataset.csv',
    'olist_products_dataset.csv',
    'olist_sellers_dataset.csv',
    'product_category_name_translation.csv'
]

for file in files:
    analyze_df(file)