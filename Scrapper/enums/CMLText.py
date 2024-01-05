from enum import Enum


class CMLText(Enum):
    PARSER = ("This command line app is created in order to ease the process of getting data from blizzard API.\n"
              "In order it to work, user need to provide his unique secret and client id, both obtainable from https://develop.battle.net/\n")
    COMMAND = "Executes one of the available command. Type -h if you wanna know more."
    COMMAND_SERVERS = "Gets the name of all valid realms and servers and creates the table out of them."
    COMMAND_ITEMS = "Downloads the basic information about items that are in the auction house."
    COMMAND_AUCTIONS = "Downloads the items from the auction houses."
    COMMAND_ITEMS_CLASS = "Downloads the data about the classes of the items from the Item.csv file."
    COMMAND_GET_MEDIA = "Downloads the data about the url to the items icons. Use after check_auction command!"

    COMMAND_CHECK_AUCTION = "Tests whether the items stored in auction are in the file containing list of items."
    COMMAND_MK_DEAD_SERVERS = ("Marks dead servers from the auction file and realms.csv files."
                               "Dead servers are considered the one that have less that 1000 transactions in total on Auction.")
    COMMAND_RM_SUS_TRANS = "Removes the suspiscius transactions (outliners) from Auction.csv."

    COMMAND_ALL = "Uses all methods that are above. This will last like dozens of minutes."
