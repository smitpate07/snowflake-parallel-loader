import snowflake.connector
import threading
import os 
from dotenv import load_dotenv
from collections import defaultdict
from snowflake_project.chunk_calc import ChunkCalc
from snowflake_project.logger import logging
from snowflake_project.utils import get_connection


class DataIngestion:
    thread_row_counts = defaultdict(int)
    def __init__(self, chunk_count):
        self.chunk_count = chunk_count

    def prepare_queries(self):
        """Generate SQL queries for each chunk."""
        queries = []
        for i in range(self.chunk_count):
            query = f"""
            INSERT INTO SNOWFLAKE_LEARNING_DB.SNOWFLAKE_TEST.STORE_SALES
            SELECT *
            FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF100TCL.STORE_SALES
            WHERE MOD(ABS(HASH(SS_SOLD_DATE_SK,SS_TICKET_NUMBER)), {self.chunk_count}) = {i};
            """
            queries.append((i, query))
        return queries

    def run_query_with_rowcount(self, chunk_info):
        """Run a query and log thread info, MOD condition, and row count inserted."""
        idx, query = chunk_info
        thread_id = threading.get_ident()
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("ALTER SESSION SET USE_CACHED_RESULT = FALSE;")
                    logging.info(f"Chunk {idx} (Thread ID {thread_id}): Starting — MOD(...) = {idx}")
                    cur.execute(query)
                    rowcount = cur.rowcount
                    logging.info(f"Chunk {idx} (Thread ID {thread_id}): Inserted {rowcount:,} rows successfully")
                    DataIngestion.thread_row_counts[thread_id] += rowcount
                    return True
        except Exception as e:
            logging.error(f"Chunk {idx} (Thread ID {thread_id}): Query failed: {e}")
            return False
