import os
from dotenv import load_dotenv

from snowflake_project.logger import logging
from snowflake_project.utils import get_connection,load_config

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
cfg = load_config(os.path.join(PROJECT_ROOT, "config", "config.yaml"))

class DataValidation:
    @staticmethod
    def verify_row_counts():
        """Verify row counts between source and target table."""
        try:
            source_count_query =  cfg['validation_queries']['source_row_count']
            target_count_query = cfg['validation_queries']['target_row_count']
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(source_count_query)
                    total_source = cur.fetchone()[0]
                    cur.execute(target_count_query)
                    total_target = cur.fetchone()[0]
                    logging.info(f"Source row count: {total_source:,}, Target row count: {total_target:,}")
                    if total_source == total_target:
                        logging.info("Row count verification PASSED.")
                    else:
                        logging.error("Row count verification FAILED.")
        except Exception as e:
            logging.error(f"Error during row count verification: {e}")
