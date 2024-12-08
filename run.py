from src.etl.pipeline import run_pipeline

if __name__ == "__main__":
    print("Starting ETL pipeline...")
    success = run_pipeline()
    
    if success:
        print("ETL pipeline completed successfully!")
    else:
        print("ETL pipeline failed. Check the logs for details.")