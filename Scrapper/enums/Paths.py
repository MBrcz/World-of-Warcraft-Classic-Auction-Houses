from enum import Enum
from os.path import join


_PATH_TO_PROJECT: str = "\\".join([f for f in __file__.split('\\')[:-2]])
_API_DUMP_PATH: str = join(_PATH_TO_PROJECT, "Data", "DownloadsFromAPI")


class Paths(Enum):
    """
    This enum file stores all paths to project directories // files
    """

    REALMS = join(_API_DUMP_PATH, "Realms.csv")
    AUCTIONS_TIME_LEFT = join(_API_DUMP_PATH, "Auction Time Left.csv")
    AUCTIONS = join(_API_DUMP_PATH, "Auction.csv")
    ITEMS = join(_API_DUMP_PATH, "Items.csv")
    AUCTIONS_US = join(_API_DUMP_PATH, "Test.csv")
    ITEMS_CLASSES = join(_API_DUMP_PATH, "Items Classes.csv")
    ITEMS_ICONS_URL = join(_API_DUMP_PATH, "Items Media.csv")
