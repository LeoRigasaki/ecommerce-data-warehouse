from sqlalchemy import create_engine
import pandas as pd

def clear_tables(engine, table_order):
    """
    Clears tables in the reverse order of dependencies to handle foreign key constraints.
    """
    with engine.connect() as connection:
        for table in reversed(table_order):  # Start from dependent tables
            try:
                connection.execute(f"TRUNCATE TABLE {table} CASCADE;")
                print(f"Cleared table {table} (CASCADE).")
            except Exception as e:
                print(f"Error clearing table {table}: {e}")

def load_data(transformed_data, db_url="postgresql://dwh_user:cls@localhost:5432/ecommerce_dwh"):
    """
    Loads the transformed data into the database in dependency order.
    """
    engine = create_engine(db_url)

    # Define the load order to respect table dependencies
    load_order = ["dim_customer", "dim_seller", "dim_product", "dim_date", "fact_orders"]

    # Clear tables before loading
    print("Clearing tables...")
    clear_tables(engine, load_order)

    # Load data
    for table_name in load_order:
        try:
            df = transformed_data[table_name]

            # Drop any 'index' column if present
            if 'index' in df.columns:
                df = df.drop(columns=['index'])

            # Write data to the table
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"Loaded {len(df)} rows into {table_name} table.")
        except Exception as e:
            print(f"Error loading data into {table_name}: {e}")

if __name__ == "__main__":
    from transform import transform_data
    from extract import extract_data

    # Extract and transform data
    print("Extracting and transforming data...")
    datasets = extract_data()
    transformed_data = transform_data(datasets)

    # Load data into the database
    print("Loading data into the database...")
    load_data(transformed_data)
