import os
from comms_helper.data.dummy import df_dummy

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
        # conn.execute(
        #     """
        #     INSERT INTO tweets ({cols})
        # SELECT {cols} FROM tweets_temp
        # ON CONFLICT (tweet_id)
        #         DO UPDATE
        #         SET
        #             import_timestamp=EXCLUDED.import_timestamp
        # """.format(
        #         cols=",".join([i for i in df_dummy.columns]),
        #         cols_set=",".join(
        #             [
        #                 "{col} = tweets_temp.{col}".format(col=i)
        #                 for i in df_dummy.columns
        #                 if i != "tweet_id"
        #             ]
        #         ),
        #     )
        # )
