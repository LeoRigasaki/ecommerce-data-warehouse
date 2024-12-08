import pandas as pd
from src.database.connection import get_connection

def analyze_sales_performance():
    """
    Analyze sales performance by calculating key metrics:
    - Total sales by month
    - Top selling products
    - Customer purchase patterns
    """
    conn = get_connection()
    
    queries = {
        "monthly_sales": """
            SELECT 
                d.year,
                d.month,
                COUNT(DISTINCT f.order_id) as total_orders,
                SUM(f.price) as total_sales
            FROM fact_orders f
            JOIN dim_date d ON f.purchase_date_key = d.date_key
            GROUP BY d.year, d.month
            ORDER BY d.year, d.month;
        """,
        
        "top_products": """
            SELECT 
                p.product_category_name_english,
                COUNT(DISTINCT f.order_id) as order_count,
                SUM(f.price) as total_revenue
            FROM fact_orders f
            JOIN dim_product p ON f.product_key = p.product_key
            GROUP BY p.product_category_name_english
            ORDER BY total_revenue DESC
            LIMIT 10;
        """,
        
        "customer_segments": """
            SELECT 
                c.customer_state,
                COUNT(DISTINCT f.order_id) as total_orders,
                COUNT(DISTINCT c.customer_key) as total_customers,
                SUM(f.price) as total_revenue
            FROM fact_orders f
            JOIN dim_customer c ON f.customer_key = c.customer_key
            GROUP BY c.customer_state
            ORDER BY total_revenue DESC;
        """
    }
    
    results = {}
    for name, query in queries.items():
        results[name] = pd.read_sql_query(query, conn)
    
    conn.close()
    return results

def get_sales_insights():
    """
    Print formatted insights from the analysis
    """
    results = analyze_sales_performance()
    
    print("\n=== Monthly Sales Trends ===")
    print(results["monthly_sales"])
    
    print("\n=== Top 10 Product Categories ===")
    print(results["top_products"])
    
    print("\n=== Customer Segments by State ===")
    print(results["customer_segments"])

if __name__ == "__main__":
    get_sales_insights()