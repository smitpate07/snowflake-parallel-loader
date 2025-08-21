import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
from snowflake_project.utils import load_config
from dotenv import load_dotenv
from snowflake_project.logger import logging
from snowflake_project.source_row_count import Source_Row_Count
from snowflake_project.data_ingestion import DataIngestion
from snowflake_project.chunk_calc import ChunkCalc
from concurrent.futures import ThreadPoolExecutor, as_completed
from snowflake_project.validation import DataValidation
from snowflake_project.chunk_summary import ChunkSummary
from snowflake_project.utils  import get_connection,load_config


def main():
    try:
        cfg = load_config(os.path.join(PROJECT_ROOT,"snowflake_project", "config", "config.yaml"))
        logging.info("Starting parallel load job")

        total_rows = Source_Row_Count.get_source_row_count()
        logging.info(f"Total rows in source table: {total_rows:,}")

        chunk_count = ChunkCalc.calculate_chunks(total_rows,cfg['chunk_calc']['min_rows_per_chunk'],cfg['chunk_calc']['max_concurrency'])

        data_ingestion = DataIngestion(chunk_count)
        truncate_sql = cfg["queries"]["truncate_table"]

        # TRUNCATE once before starting inserts
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(truncate_sql)
                logging.info("Target table truncated before load.")

        queries = data_ingestion.prepare_queries()

        with ThreadPoolExecutor(max_workers=chunk_count) as executor:
            future_to_idx = {executor.submit(data_ingestion.run_query_with_rowcount, q): q[0] for q in queries}
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                if not future.result():
                    logging.error(f"Chunk {idx} failed.")

        data_validation = DataValidation.verify_row_counts()

        ChunkSummary.chunk_summary()
        logging.info("Parallel load job completed.")

    except Exception as e:
        raise e

if __name__=='__main__':
    main()