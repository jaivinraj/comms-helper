import os
from comms_helper.data.dummy import df_dummy
from comms_helper.data.update_tables import scrape_to_database

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")

from comms_helper.data.create_database import create_schema, CREATE_TABLE_QUERY
from comms_helper.data.update_tables import Q_UPDATE_TWEETS
from comms_helper.data.db_utils import get_engine, schema_exists


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


def test_update_tweets():
    engine = get_engine(user, password, schema="testing")
    with engine.connect() as conn:
        # create temporary table
        conn.execute("CREATE TEMPORARY TABLE tweets_temp (LIKE tweets)")
        # add incoming to temporary table
        df_dummy.to_sql(
            con=conn,
            name="tweets_temp",
            if_exists="append",
            index=False,
        )
        # join to full table
        conn.execute(Q_UPDATE_TWEETS)


def test_update_tweets_scrape():
    scrape_to_database("Robert Hazell", user=user, password=password, n_max=20)


def test_schema_exists():
    # check made up schema doesn't exist
    assert not schema_exists("made_up_schema", user, password)
    create_schema("test_schema", user, password)
    assert schema_exists("test_schema", user, password)
    engine = get_engine(user, password)
    with engine.connect() as conn:
        conn.execute(f"DROP SCHEMA test_schema CASCADE")
