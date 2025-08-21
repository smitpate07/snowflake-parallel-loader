from snowflake_project.logger import logging
from snowflake_project.data_ingestion import DataIngestion


class ChunkSummary:
    try:
        @staticmethod
        def chunk_summary():
            """Log a summary of rows processed by each thread."""
            logging.info("=" * 50)
            logging.info("FINAL ROW COUNT SUMMARY PER THREAD")
            for tid, count in DataIngestion.thread_row_counts.items():
                logging.info(f"Thread ID {tid}: {count:,} rows inserted")
            total_inserted = sum(DataIngestion.thread_row_counts.values())
            logging.info(f"TOTAL rows inserted across all threads: {total_inserted:,}")
            logging.info("=" * 50)
    except Exception as e:
        raise e
