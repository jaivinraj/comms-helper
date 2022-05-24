import pandas as pd

entities = {
    "Jaivin": "jaivinraj",
    "Greta": "gretathunberg",
    "Owen": "owenjones84",
    "Jonas": "tenorkaufmann",
}
df_dummy = pd.DataFrame(
    {
        "url": ["https://twitter.com/thisisnotaurl{}".format(i) for i in range(4)],
        "timestamp": [pd.to_datetime("2022-01-0{}".format(i)) for i in range(1, 5)],
        "content": [
            "hello I am {} @{}".format(key, val) for key, val in entities.items()
        ],
        "username": [i for i in entities.values()],
        "tweet_id": [i for i in range(4)],
        "import_timestamp": [pd.Timestamp.now() for i in range(4)],
    }
)
