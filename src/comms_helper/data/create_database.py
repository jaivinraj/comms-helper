from functools import partial
from comms_helper.logging_utils import log_with_prefix
from comms_helper.data.db_utils import get_engine

logging_prefix = "comms_helper.analysis.network"

log_with_mod_prefix = partial(log_with_prefix, logging_prefix=logging_prefix)

# Query generated from lucid
CREATE_TABLE_QUERY = """
CREATE TABLE "tweets" (
  "tweet_id" BIGINT,
  "content" TEXT,
  "url" TEXT,
  "username" VARCHAR(15),
  "timestamp" TIMESTAMP,
  "import_timestamp" TIMESTAMP,
  PRIMARY KEY ("tweet_id")
);

CREATE TABLE "mentions" (
  "tweet_id" BIGINT,
  "username" VARCHAR(15),
  CONSTRAINT "FK_mentions.tweet_id"
    FOREIGN KEY ("tweet_id")
      REFERENCES "tweets"("tweet_id")
);

CREATE TABLE "searches" (
  "search_id" INT,
  "search_content" TEXT,
  PRIMARY KEY ("search_id")
);

CREATE TABLE "tweet_searches" (
  "tweet_id" BIGINT,
  "search_id" INT,
  CONSTRAINT "FK_tweet_searches.search_id"
    FOREIGN KEY ("search_id")
      REFERENCES "searches"("search_id"),
  CONSTRAINT "FK_tweet_searches.tweet_id"
    FOREIGN KEY ("tweet_id")
      REFERENCES "tweets"("tweet_id")
);


"""


def create_schema(schema_name, user, password):
    engine = get_engine(user, password)
    log_with_mod_prefix("Creating schema if doesn't exist...")
    with engine.connect() as conn:
        conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
