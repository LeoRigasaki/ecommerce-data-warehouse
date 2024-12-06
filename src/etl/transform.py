import pandas as pd
from extract import extract_data

def clean_customer_data(customers_df):
    """
    Cleans and transforms customer data.
    
    We perform several cleaning operations:
    1. Remove duplicates
    2. Convert city and state names to title case
    3. Ensure all text fields have consistent casing
    4. Handle any missing values
    """
    customers_clean = customers_df.copy()
    
    # Remove duplicates
    customers_clean = customers_clean.drop_duplicates()
    
    # Clean text fields
    text_columns = ['customer_city', 'customer_state']
    for col in text_columns:
        customers_clean[col] = customers_clean[col].str.title()
    
    # Handle missing values
    customers_clean = customers_clean.fillna({
        'customer_city': 'Unknown',
        'customer_state': 'NA'
    })
    
    return customers_clean

def clean_seller_data(sellers_df):
    """
    Cleans and transforms seller data.
    
    Similar to customer data cleaning, we:
    1. Remove duplicates
    2. Standardize text fields
    3. Handle missing values
    """
    sellers_clean = sellers_df.copy()
    
    # Remove duplicates
    sellers_clean = sellers_clean.drop_duplicates()
    
    # Clean text fields
    text_columns = ['seller_city', 'seller_state']
    for col in text_columns:
        sellers_clean[col] = sellers_clean[col].str.title()
    
    # Handle missing values
    sellers_clean = sellers_clean.fillna({
        'seller_city': 'Unknown',
        'seller_state': 'NA'
    })
    
    return sellers_clean

def clean_product_data(products_df, categories_df):
    """
    Cleans and transforms product data.
    
    We perform several operations:
    1. Merge with category translations
    2. Clean numeric fields
    3. Handle missing values
    4. Remove invalid entries
    """
    products_clean = products_df.copy()
    
    # Merge with category translations
    products_clean = products_clean.merge(
        categories_df,
        on='product_category_name',
        how='left'
    )
    
    # Convert numeric fields to appropriate types
    numeric_columns = [
        'product_name_lenght', 'product_description_lenght',
        'product_photos_qty', 'product_weight_g',
        'product_length_cm', 'product_height_cm',
        'product_width_cm'
    ]
    
    for col in numeric_columns:
        products_clean[col] = pd.to_numeric(products_clean[col], errors='coerce')
    
    # Handle missing values
    products_clean = products_clean.fillna({
        'product_category_name': 'unknown',
        'product_category_name_english': 'unknown',
        'product_name_lenght': 0,
        'product_description_lenght': 0,
        'product_photos_qty': 0,
        'product_weight_g': 0,
        'product_length_cm': 0,
        'product_height_cm': 0,
        'product_width_cm': 0
    })
    
    return products_clean

def prepare_order_data(orders_df, order_items_df):
    """
    Prepares order data by combining orders and order items.
    
    This function:
    1. Merges order and order items data
    2. Cleans date fields
    3. Handles missing values
    4. Validates numeric fields
    """
    # Convert date columns to datetime
    date_columns = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date',
        'shipping_limit_date'
    ]
    
    orders_clean = orders_df.copy()
    order_items_clean = order_items_df.copy()
    
    for col in date_columns:
        if col in orders_clean.columns:
            orders_clean[col] = pd.to_datetime(orders_clean[col], errors='coerce')
    
    order_items_clean['shipping_limit_date'] = pd.to_datetime(
        order_items_clean['shipping_limit_date'],
        errors='coerce'
    )
    
    # Merge orders with order items
    orders_combined = orders_clean.merge(
        order_items_clean,
        on='order_id',
        how='left'
    )
    
    # Clean numeric fields
    orders_combined['price'] = pd.to_numeric(orders_combined['price'], errors='coerce')
    orders_combined['freight_value'] = pd.to_numeric(orders_combined['freight_value'], errors='coerce')
    
    # Handle missing values
    orders_combined = orders_combined.fillna({
        'order_status': 'unknown',
        'price': 0,
        'freight_value': 0
    })
    
    return orders_combined

def transform_data():
    """
    Main transformation function that coordinates all cleaning operations.
    """
    try:
        # Extract raw data
        customers_df, orders_df, order_items_df, products_df, sellers_df, categories_df = extract_data()
        
        # Clean dimension tables
        clean_customers = clean_customer_data(customers_df)
        clean_sellers = clean_seller_data(sellers_df)
        clean_products = clean_product_data(products_df, categories_df)
        
        # Prepare fact table data
        clean_orders = prepare_order_data(orders_df, order_items_df)
        
        print("Data transformation completed successfully!")
        
        return clean_customers, clean_sellers, clean_products, clean_orders
        
    except Exception as e:
        print(f"Error in data transformation: {str(e)}")
        raise

if __name__ == "__main__":
    # Test the transformation
    transform_data()