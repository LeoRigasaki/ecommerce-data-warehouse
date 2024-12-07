import pandas as pd

def transform_data(datasets):
    # --- Transform dim_customer ---
    dim_customer = datasets['customers'][[
        'customer_id',
        'customer_unique_id',
        'customer_zip_code_prefix',
        'customer_city',
        'customer_state'
    ]].copy()
    dim_customer['created_at'] = pd.Timestamp.now()
    dim_customer.reset_index(inplace=True)  # Ensure customer_key matches index

    # --- Transform dim_seller ---
    dim_seller = datasets['sellers'][[
        'seller_id',
        'seller_zip_code_prefix',
        'seller_city',
        'seller_state'
    ]].copy()
    dim_seller['created_at'] = pd.Timestamp.now()
    dim_seller.reset_index(inplace=True)  # Ensure seller_key matches index

    # --- Transform dim_product ---
    dim_product = datasets['products'][[
        'product_id',
        'product_category_name',
        'product_weight_g',
        'product_length_cm',
        'product_height_cm',
        'product_width_cm'
    ]].copy()
    category_translation = datasets['category_translation']
    dim_product = dim_product.merge(
        category_translation,
        on='product_category_name',
        how='left'
    )
    dim_product.fillna({
        'product_weight_g': 0,
        'product_length_cm': 0,
        'product_height_cm': 0,
        'product_width_cm': 0,
        'product_category_name_english': 'unknown'
    }, inplace=True)
    dim_product['created_at'] = pd.Timestamp.now()
    dim_product.reset_index(inplace=True)  # Ensure product_key matches index

    # --- Transform dim_date ---
    date_columns = ['order_purchase_timestamp', 'order_approved_at',
                    'order_delivered_carrier_date', 'order_delivered_customer_date']
    dates = pd.concat(
        [pd.to_datetime(datasets['orders'][col], errors='coerce') for col in date_columns]
    ).dropna().drop_duplicates()
    dim_date = pd.DataFrame({'date_actual': dates})
    dim_date['date_actual'] = dim_date['date_actual'].dt.date  # Normalize to date only
    dim_date['year'] = pd.to_datetime(dim_date['date_actual']).dt.year
    dim_date['month'] = pd.to_datetime(dim_date['date_actual']).dt.month
    dim_date['day'] = pd.to_datetime(dim_date['date_actual']).dt.day
    dim_date['quarter'] = pd.to_datetime(dim_date['date_actual']).dt.quarter
    dim_date['day_of_week'] = pd.to_datetime(dim_date['date_actual']).dt.dayofweek + 1
    dim_date['is_weekend'] = dim_date['day_of_week'].isin([6, 7])
    dim_date['created_at'] = pd.Timestamp.now()

    # Ensure uniqueness
    dim_date = dim_date.drop_duplicates(subset=['date_actual']).reset_index(drop=True)
    dim_date.reset_index(inplace=True)  # Ensure date_key matches index

    # --- Transform fact_orders ---
    fact_orders = datasets['order_items'][[
        'order_id', 'order_item_id', 'product_id', 'seller_id',
        'shipping_limit_date', 'price', 'freight_value'
    ]].merge(
        datasets['orders'][[
            'order_id', 'customer_id', 'order_status', 'order_purchase_timestamp'
        ]],
        on='order_id',
        how='inner'
    )

    # Set indices for efficient join
    dim_product.set_index('product_id', inplace=True)
    dim_customer.set_index('customer_id', inplace=True)
    dim_seller.set_index('seller_id', inplace=True)
    dim_date.set_index('date_actual', inplace=True)

    # Replace product_id, seller_id, and customer_id with keys
    fact_orders['product_key'] = fact_orders['product_id'].map(dim_product['index'])
    fact_orders['customer_key'] = fact_orders['customer_id'].map(dim_customer['index'])
    fact_orders['seller_key'] = fact_orders['seller_id'].map(dim_seller['index'])

    # Drop rows with missing keys
    fact_orders = fact_orders.dropna(subset=['product_key', 'customer_key', 'seller_key'])

    # Normalize timestamps and map purchase_date_key
    fact_orders['order_purchase_timestamp'] = pd.to_datetime(
        fact_orders['order_purchase_timestamp'], errors='coerce'
    ).dt.date
    fact_orders['purchase_date_key'] = fact_orders['order_purchase_timestamp'].map(dim_date['index'])

    # Remove rows with missing purchase_date_key
    fact_orders = fact_orders.dropna(subset=['purchase_date_key'])

    # Final fact_orders columns
    fact_orders = fact_orders[[
        'order_id', 'customer_key', 'seller_key', 'product_key',
        'order_item_id', 'order_status', 'purchase_date_key', 'price', 'freight_value'
    ]]
    fact_orders['created_at'] = pd.Timestamp.now()

    return {
        "dim_customer": dim_customer.reset_index(),
        "dim_seller": dim_seller.reset_index(),
        "dim_product": dim_product.reset_index(),
        "dim_date": dim_date.reset_index(),
        "fact_orders": fact_orders
    }

if __name__ == "__main__":
    from extract import extract_data
    datasets = extract_data()
    transformed_data = transform_data(datasets)
    for name, df in transformed_data.items():
        print(f"{name} table transformed with {len(df)} rows.")
