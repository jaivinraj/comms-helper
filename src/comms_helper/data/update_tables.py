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
