from venv import create
from comms_helper.data.db_utils import get_engine, schema_exists
from comms_helper.data.scraping import scrape_tweets, scraped_tweets_to_df
from comms_helper.data.create_database import create_schema, CREATE_TABLE_QUERY
import pandas as pd

Q_UPDATE_TWEETS = """
INSERT INTO tweets ({cols})
SELECT {cols} FROM tweets_temp
ON CONFLICT (tweet_id)
        DO UPDATE
        SET
            import_timestamp=EXCLUDED.import_timestamp
""".format(
    cols="""url,
timestamp,
content,
username,
tweet_id,
import_timestamp"""
)


def scrape_to_database(search, n_max=5000, schema="testing", user=None, password=None):
    # scrape data and update database
    tweets_lst = scrape_tweets(search, n_max)
    df = scraped_tweets_to_df(tweets_lst)
    df["import_timestamp"] = pd.Timestamp.now()
    engine = get_engine(user, password, schema=schema)
    with engine.connect() as conn:
        # create temporary table
        conn.execute("CREATE TEMPORARY TABLE tweets_temp (LIKE tweets)")
        # add incoming to temporary table
        df.to_sql(
            con=conn,
            name="tweets_temp",
            if_exists="append",
            index=False,
        )
        # join to full table
        conn.execute(Q_UPDATE_TWEETS)


def create_schema_and_tables(schema="testing", user=None, password=None):
    # create the schema if doesn't already exist
    if not schema_exists(schema, user, password):
        create_schema(schema, user, password)
        engine = get_engine(user, password, schema=schema)
        with engine.connect() as conn:
            conn.execute(CREATE_TABLE_QUERY)
