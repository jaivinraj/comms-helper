import os
from comms_helper.data.dummy import df_dummy
from comms_helper.data.update_tables import scrape_to_database

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")

from comms_helper.data.create_database import create_schema, CREATE_TABLE_QUERY
from comms_helper.data.update_tables import Q_UPDATE_TWEETS
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
