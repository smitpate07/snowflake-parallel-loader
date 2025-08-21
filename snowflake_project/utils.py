import yaml
import snowflake.connector
from snowflake_project.config.settings import SNOWFLAKE_CONFIG

def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_connection():
    """Return a new Snowflake connection using centralized config."""
    return snowflake.connector.connect(**SNOWFLAKE_CONFIG)