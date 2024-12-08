import pandas as pd
from src.database.connection import get_connection

def run_data_quality_checks():
    """
    Run basic data quality checks on our warehouse
    """
    conn = get_connection()
    
    checks = {
        "fact_order_counts": """
            SELECT 'Fact Orders' as table_name, 
                   COUNT(*) as row_count,
                   COUNT(DISTINCT order_id) as unique_orders
            FROM fact_orders;
        """,
        
        "dimension_counts": """
            SELECT 'Products' as dimension, COUNT(*) as count FROM dim_product
            UNION ALL
            SELECT 'Customers', COUNT(*) FROM dim_customer
            UNION ALL
            SELECT 'Sellers', COUNT(*) FROM dim_seller
            UNION ALL
            SELECT 'Dates', COUNT(*) FROM dim_date;
        """,
        
        "null_checks": """
            SELECT 'Fact Orders - Null Keys' as check_name,
                   SUM(CASE WHEN customer_key IS NULL THEN 1 ELSE 0 END) as null_customers,
                   SUM(CASE WHEN product_key IS NULL THEN 1 ELSE 0 END) as null_products,
                   SUM(CASE WHEN seller_key IS NULL THEN 1 ELSE 0 END) as null_sellers
            FROM fact_orders;
        """
    }
    
    results = {}
    for name, query in checks.items():
        results[name] = pd.read_sql_query(query, conn)
    
    conn.close()
    return results

def print_quality_report():
    """
    Print a formatted data quality report
    """
    results = run_data_quality_checks()
    
    print("\n=== Data Quality Report ===")
    for name, df in results.items():
        print(f"\n{name}:")
        print(df)

if __name__ == "__main__":
    print_quality_report()