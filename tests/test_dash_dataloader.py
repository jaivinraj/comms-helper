from comms_helper.dashboard.dataloading import DashDataFromScrape

SEARCH_TERM = "Robert Hazell"
N_MAX = 10
def test_data_from_scrape():
    dataloader = DashDataFromScrape(SEARCH_TERM,N_MAX)

    dataloader.get_tweets()