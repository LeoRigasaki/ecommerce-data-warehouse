from .transform import transform_data
from .extract import extract_data
from .load import load_data
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_pipeline():
    """
    Orchestrates the ETL pipeline in three simple steps.
    Includes basic logging to track progress.
    """
    try:
        # Step 1: Extract
        logger.info("Starting data extraction...")
        datasets = extract_data()
        logger.info("Data extraction completed.")

        # Step 2: Transform
        logger.info("Starting data transformation...")
        transformed_data = transform_data(datasets)
        logger.info("Data transformation completed.")

        # Step 3: Load
        logger.info("Starting data loading...")
        load_data(transformed_data)
        logger.info("Data loading completed.")
        
        return True

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        return False