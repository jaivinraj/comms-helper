from abc import ABC, abstractmethod


from comms_helper.data.scraping import (
    scrape_tweets,
    scraped_tweets_to_df,
)

from comms_helper.data.db_utils import get_engine
import pandas as pd


class DashData(ABC):
    """Abstract base class for propagating continuous assessment scores

    Parameters
    ----------
    skills : iterable
        Iterable containing the names of the skills which can be assessed
    levels: iterable
        Current levels for each skill
    obs_rate: iterable
        Measure of density of observations that led to each level
    """

    def __init__(self, searchname):
        self.searchname = searchname

    @abstractmethod
    def get_tweets(self):
        pass


class DashDataFromScrape(DashData):
    def __init__(self, searchname="Robert Hazell", n_max=20):
        super().__init__(searchname)
        self.n_max = n_max

    def get_tweets(self):
        tweets_lst = scrape_tweets(self.searchname, self.n_max)
        return scraped_tweets_to_df(tweets_lst)


class DashDataFromDatabase(DashData):
    def __init__(self, searchname="Robert Hazell", user=None, password=None):
        super().__init__(searchname)
        self.__user = user
        self.__password = password
        self.engine = get_engine(self.__user, self.__password, schema="tweets")

    def get_tweets(self):
        with self.engine.connect() as conn:
            df = pd.read_sql("SELECT * FROM tweets", con=conn)
        return df
