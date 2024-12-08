# Olist E-commerce Data Warehouse Project

## Project Overview
This project implements a data warehouse solution for the Brazilian E-commerce Public Dataset by Olist. The data warehouse transforms Olist's transactional data into a dimensional model optimized for business intelligence and analysis.

## Data Warehouse Architecture

### Star Schema Design
Our data warehouse implements a star schema with the following structure:

- **Fact Table**: fact_orders
  - Contains order transactions with foreign keys to dimension tables
  - Includes metrics like price and freight value

- **Dimension Tables**:
  - dim_customer: Customer information and demographics
  - dim_seller: Seller details and locations
  - dim_product: Product information and categories
  - dim_date: Date dimension for time-based analysis

## Project Structure

```
ecommerce-data-warehouse/
├── config/
│   └── database.ini          # Database configuration
├── data/
│   ├── processed/            # Transformed data files
│   └── raw/                  # Original Olist CSV files
├── notebooks/
│   └── data_warehouse_analysis.ipynb    # Analysis and visualizations
├── src/
│   ├── analysis/
│   │   └── business_queries.py          # Business intelligence queries
│   ├── database/
│   │   ├── connection.py                # Database connection handling
│   │   └── schema.sql                   # Data warehouse schema definition
│   ├── etl/
│   │   ├── extract.py                   # Data extraction from CSV files
│   │   ├── transform.py                 # Data transformation logic
│   │   ├── load.py                      # Database loading operations
│   │   └── pipeline.py                  # ETL orchestration
│   └── utils/
│       ├── data_quality.py              # Data quality validation
│       └── helpers.py                   # Helper functions
├── tests/                               # Test files
├── requirements.txt                     # Project dependencies
└── run.py                              # Main execution script
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- Virtual environment management tool (venv recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/LeoRigasaki/ecommerce-data-warehouse.git
   cd ecommerce-data-warehouse
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure database:
   - Create a PostgreSQL database
   - Copy config/database.ini.example to config/database.ini
   - Update database.ini with your credentials

### Database Setup
1. Create the database schema:
   ```bash
   psql -U your_username -d your_database -f src/database/schema.sql
   ```
![Database Schema Diagram](src/database/diagram/schema.png)
## Usage

### Running the ETL Pipeline
Execute the complete ETL process:
```bash
python run.py
```

### Data Quality Checks
Run data quality validations:
```bash
python -m src.utils.data_quality
```

### Business Analysis
Generate business insights:
```bash
python -m src.analysis.business_queries
```

## Data Analysis and Visualization
The project includes a Jupyter notebook (`notebooks/data_warehouse_analysis.ipynb`) that demonstrates:
- Order trends analysis
- Customer segmentation
- Product category performance
- Geographical distribution of sales

## Key Features

### ETL Pipeline
- Extracts data from multiple CSV files
- Transforms raw data into dimensional model
- Loads data into PostgreSQL database
- Includes data quality validation

### Data Quality Checks
- Validates data completeness
- Ensures referential integrity
- Verifies business rules
- Reports data quality metrics

### Business Intelligence
- Provides pre-built analysis queries
- Supports custom query development
- Enables complex business analysis

## Future Development
The main branch serves as the foundation for exploring various data warehousing tools. Future branches will implement:
- DBT for data transformation
- Apache Airflow for workflow orchestration
- Docker for containerization

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Dataset provided by Olist Store
- Brazilian E-commerce Public Dataset by Olist on Kaggle