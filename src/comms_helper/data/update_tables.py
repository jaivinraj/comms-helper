from comms_helper.data.db_utils import get_engine
from comms_helper.data.scraping import scrape_tweets, scraped_tweets_to_df
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
    tweets_lst = scrape_tweets(search, n_max)
    df = scraped_tweets_to_df(tweets_lst)
    df["import_timestamp"] = pd.Timestamp.now()
    engine = get_engine(user, password, schema="testing")
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
