import pandas as pd

def extract_data():
    file_paths = {
        "order_items": "data/raw/olist_order_items_dataset.csv",
        "orders": "data/raw/olist_orders_dataset.csv",
        "products": "data/raw/olist_products_dataset.csv",
        "customers": "data/raw/olist_customers_dataset.csv",
        "category_translation": "data/raw/product_category_name_translation.csv",
        "sellers": "data/raw/olist_sellers_dataset.csv"
    }

    datasets = {name: pd.read_csv(path) for name, path in file_paths.items()}
    return datasets

if __name__ == "__main__":
    datasets = extract_data()
    for name, df in datasets.items():
        print(f"{name} dataset loaded with {len(df)} rows.")
