import pandas as pd
import os

def extract_data():
    """
    Extracts data from CSV files and returns DataFrames.
    
    Returns:
        tuple: DataFrames for customers, orders, order_items, products, 
               sellers, and categories
    """
    # Define the base path for data files
    base_path = 'data/raw'
    
    # Read each CSV file
    try:
        customers_df = pd.read_csv(
            os.path.join(base_path, 'olist_customers_dataset.csv')
        )
        orders_df = pd.read_csv(
            os.path.join(base_path, 'olist_orders_dataset.csv')
        )
        order_items_df = pd.read_csv(
            os.path.join(base_path, 'olist_order_items_dataset.csv')
        )
        products_df = pd.read_csv(
            os.path.join(base_path, 'olist_products_dataset.csv')
        )
        sellers_df = pd.read_csv(
            os.path.join(base_path, 'olist_sellers_dataset.csv')
        )
        categories_df = pd.read_csv(
            os.path.join(base_path, 'product_category_name_translation.csv')
        )
        
        print("Data extraction completed successfully!")
        
        return (
            customers_df, orders_df, order_items_df,
            products_df, sellers_df, categories_df
        )
        
    except Exception as e:
        print(f"Error extracting data: {str(e)}")
        raise

if __name__ == "__main__":
    # Test the extraction
    extract_data()