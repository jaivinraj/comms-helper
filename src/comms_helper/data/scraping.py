"""Functions for scraping Twitter data"""
import snscrape.modules.twitter as sntwitter
import pandas as pd
from tqdm import tqdm
from functools import partial


from comms_helper.logging_utils import log_with_prefix

logging_prefix = "comms_helper.scraping"

log_with_mod_prefix = partial(log_with_prefix, logging_prefix=logging_prefix)


def scrape_tweets(search, n_max=5000):
    """Scrape tweets from a search into a Python list

    Parameters
    ----------
    search : str
        Twitter search (eg. "Elon Musk")
    n_max : int, optional
        Maximum number of tweets to fetch (set to a v large int to fetch all), by default 5000

    Returns
    -------
    list
        List of scraper objects, where each item represents a tweet
    """
    log_with_mod_prefix(
        "Scraping the first {} tweets for search '{}'...".format(n_max, search)
    )
    # Creating list to append tweet data to
    tweets_list = []
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in tqdm(
        enumerate(sntwitter.TwitterSearchScraper("{}".format(search)).get_items()),
        total=n_max,
    ):
        if i > n_max:
            break
        tweets_list += [tweet]
    log_with_mod_prefix(
        "Scraped {:,} tweets".format(len(tweets_list))
    )
    return tweets_list


def scraped_tweets_to_df(tweets_list):
    """Convert list of scraped tweets to a dataframe

    Parameters
    ----------
    tweets_list : list
        List of scraper objects, where each item represents a tweet

    Returns
    -------
    pd.DataFrame
        Dataframe representing the scraped tweets
    """
    log_with_mod_prefix("Converting scraped tweets into a dataframe", level="debug")
    tweet_dict = {}

    tweet_dict["url"] = [tweet.url for tweet in tweets_list]

    tweet_dict["date"] = [tweet.date for tweet in tweets_list]

    tweet_dict["content"] = [tweet.content for tweet in tweets_list]

    tweet_dict["id"] = [tweet.id for tweet in tweets_list]

    tweet_dict["username"] = [tweet.username for tweet in tweets_list]
    return pd.DataFrame(tweet_dict)


# def scrape_tweets_to_df(search, n_max=5000):
#     tweets_lst = scrape_tweets(search, n_max)
#     return scrape_tweets_to_df(tweets_lst)
