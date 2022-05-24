import os
from venv import create

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")

from comms_helper.data.create_database import create_schema, CREATE_TABLE_QUERY
from comms_helper.data.db_utils import get_engine


def test_create_schema():
    create_schema("testing", user, password)
    engine = get_engine(user, password)
    with engine.connect() as conn:
        conn.execute(f"DROP SCHEMA testing CASCADE")


def test_create_tables():
    create_schema("testing", user, password)
    engine = get_engine(user, password, schema="testing")
    with engine.connect() as conn:
        conn.execute(CREATE_TABLE_QUERY)
