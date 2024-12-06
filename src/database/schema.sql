-- Dimension Tables
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix VARCHAR(10),
    customer_city VARCHAR(100),
    customer_state CHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_seller (
    seller_key SERIAL PRIMARY KEY,
    seller_id VARCHAR(50) UNIQUE NOT NULL,
    seller_zip_code_prefix VARCHAR(10),
    seller_city VARCHAR(100),
    seller_state CHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    product_category_name VARCHAR(100),
    product_category_name_english VARCHAR(100),
    product_name_length INTEGER,
    product_description_length INTEGER,
    product_photos_qty INTEGER,
    product_weight_g INTEGER,
    product_length_cm INTEGER,
    product_height_cm INTEGER,
    product_width_cm INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_date (
    date_key SERIAL PRIMARY KEY,
    date_actual DATE UNIQUE NOT NULL,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    quarter INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fact Table
CREATE TABLE fact_orders (
    order_key SERIAL PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    seller_key INTEGER REFERENCES dim_seller(seller_key),
    product_key INTEGER REFERENCES dim_product(product_key),
    order_item_id INTEGER,
    order_status VARCHAR(20),
    purchase_date_key INTEGER REFERENCES dim_date(date_key),
    approved_date_key INTEGER REFERENCES dim_date(date_key),
    carrier_date_key INTEGER REFERENCES dim_date(date_key),
    delivery_date_key INTEGER REFERENCES dim_date(date_key),
    estimated_delivery_date_key INTEGER REFERENCES dim_date(date_key),
    shipping_limit_date_key INTEGER REFERENCES dim_date(date_key),
    price DECIMAL(10,2),
    freight_value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_fact_orders_order_id ON fact_orders(order_id);
CREATE INDEX idx_fact_orders_customer ON fact_orders(customer_key);
CREATE INDEX idx_fact_orders_seller ON fact_orders(seller_key);
CREATE INDEX idx_fact_orders_product ON fact_orders(product_key);
CREATE INDEX idx_fact_orders_purchase_date ON fact_orders(purchase_date_key);