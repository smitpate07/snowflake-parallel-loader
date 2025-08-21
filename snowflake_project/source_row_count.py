import os
from dotenv import load_dotenv
from snowflake_project.utils import get_connection,load_config

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
cfg = load_config(os.path.join(PROJECT_ROOT, "config", "config.yaml"))

class Source_Row_Count:
    try:
        def get_source_row_count():
            """Count rows in the source table."""
            sql = cfg["queries"]["source_row_count"]
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    return cur.fetchone()[0]
    except Exception as e:
        raise e