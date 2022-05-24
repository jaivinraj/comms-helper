from comms_helper.data.scraping import (
    scrape_tweets,
    scraped_tweets_to_df,
)

SEARCH_TERM = "Robert Hazell"
N_MAX = 10
def test_scrape_tweets():
    tweets_lst = scrape_tweets(SEARCH_TERM, N_MAX)
    assert len(tweets_lst) == N_MAX