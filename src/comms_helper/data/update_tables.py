from venv import create
from comms_helper.data.db_utils import get_engine, schema_exists
from comms_helper.data.scraping import scrape_tweets, scraped_tweets_to_df
from comms_helper.data.create_database import create_schema, CREATE_TABLE_QUERY
import pandas as pd
from comms_helper.preprocessing.handle_extraction import extract_handles

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

Q_UPDATE_MENTIONS = """
INSERT INTO mentions ({cols})
SELECT {cols} FROM mentions_temp
ON CONFLICT (tweet_id,username)
        DO NOTHING
""".format(
    cols="""tweet_id,
    username"""
)


def scrape_to_database(
    search, n_max=5000, schema="testing", user=None, password=None, start_date=None
):
    # scrape data and update database
    tweets_lst = scrape_tweets(
        search
        + (
            "since {}".format(start_date.strftime("%m/%d/%Y"))
            if start_date is not None
            else ""
        ),
        n_max,
    )
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
        # get mentions
        df_mentions = pd.read_sql(
            "SELECT tweet_id,content FROM tweets_temp", con=conn
        ).set_index("tweet_id")
        mentions = (
            extract_handles(df_mentions["content"]).to_frame("username").reset_index()
        )
        # create temporary table
        conn.execute("CREATE TEMPORARY TABLE mentions_temp (LIKE mentions)")
        mentions.to_sql(
            con=conn,
            name="mentions_temp",
            if_exists="append",
            index=False,
        )

        # join all to full table
        conn.execute(Q_UPDATE_TWEETS)
        conn.execute(Q_UPDATE_MENTIONS)


def create_schema_and_tables(schema="testing", user=None, password=None):
    # create the schema if doesn't already exist
    if not schema_exists(schema, user, password):
        create_schema(schema, user, password)
        engine = get_engine(user, password, schema=schema)
        with engine.connect() as conn:
            conn.execute(CREATE_TABLE_QUERY)
