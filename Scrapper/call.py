# In  built imports
import argparse

# UDF Imports
from enums.CMLText import CMLText as T
from enums.CMLCommands import CMLCommands as C


"""
This file stores the cml application logic in relation to getting the data from Blizzard API.
"""
# -------------------------------------------------------------------------------------------------
# -------------------------------- COMMANDS -------------------------------------------------------
# -------------------------------------------------------------------------------------------------


def get_server_names() -> None:
    """
    Downloads from the blizzard API the name of all servers. Output is saved in DIR Data/DownloadsFromAPI

    :return: None
    """

    from functions.getFromAPI import create_table_of_valid_realms
    create_table_of_valid_realms()


def get_item_data() -> None:
    """
    Downloads the basic data about the items from WoW API. Output is saved in Dir Data/DownloadsFromAPI

    :return: None
    """

    from functions.getFromAPI import download_items_data_from_web
    download_items_data_from_web()


def get_auctions_data() -> None:
    """
    Downlaods the data about current auctions from WoW API. Output is saved in Dir Data/DownloadsFromAPI

    :return: None
    """

    from functions.getFromAPI import download_auction_data_from_web
    download_auction_data_from_web()


def get_class_item_ids() -> None:
    """
    Downloads the data about the class id's of the items. Output is saved in Dir Data/DownloadsFromAPI

    :return: None
    """

    from functions.getFromAPI import download_class_and_subclass_descriptions_from_web
    download_class_and_subclass_descriptions_from_web()


def get_items_media() -> None:
    """
    Gets the media (urls to the icons) of the items. Output is saved in Dir Data/DownloadsFromAPI

    :return: None
    """

    from functions.getFromAPI import download_item_media_description_from_web
    download_item_media_description_from_web()


def check_items() -> None:
    """
    Removes from auction file transactions that are related to the items that do not exist in Items.csv.

    :return: None
    """

    from functions.preProcessData import check_items
    check_items()


def mark_dead_servers() -> None:
    """
    Marks the dead servers from the data files. The dead servers are the one considered that have less
    than 1000 transactions in total

    :return: None
    """

    from functions.preProcessData import mark_dead_servers
    mark_dead_servers()


def remove_suspiscious_transaction() -> None:
    """
    Removes the suspicious transactions from Auctions.csv. For more info see into the function.

    :return: None
    """

    # NOT IMPLEMENTED!
    from functions.preProcessData import remove_suspicious_transactions
    remove_suspicious_transactions()

# -------------------------------------------------------------------------------------------------
# -------------------------------- PARSER ---------------------------------------------------------
# -------------------------------------------------------------------------------------------------


parser = argparse.ArgumentParser(description=T.PARSER.value)
subparser = parser.add_subparsers(dest=C.COMMAND.value, help=T.COMMAND.value)


serv_parser = subparser.add_parser(C.COMMAND_SERVER.value, help=T.COMMAND_SERVERS.value)
items_parser = subparser.add_parser(C.COMMAND_ITEMS.value, help=T.COMMAND_ITEMS.value)
auction_parser = subparser.add_parser(C.COMMAND_AUCTIONS.value, help=T.COMMAND_AUCTIONS.value)
class_id_parser = subparser.add_parser(C.COMMAND_ITEMS_CLASS.value, help=T.COMMAND_ITEMS_CLASS.value)
items_media_parser = subparser.add_parser(C.COMMAND_GET_MEDIA.value, help=T.COMMAND_GET_MEDIA.value)

clear_auction_parser = subparser.add_parser(C.COMMAND_CHECK_AUCTION.value, help=T.COMMAND_CHECK_AUCTION.value)
mk_dead_servers_parser = subparser.add_parser(C.COMMAND_MK_DEAD_SERVERS.value, help=T.COMMAND_MK_DEAD_SERVERS.value)
rm_sus_trans_parser = subparser.add_parser(C.COMMAND_RM_SUS_TRANS.value, help=T.COMMAND_RM_SUS_TRANS.value)

all_parser = subparser.add_parser(C.COMMAND_ALL.value, help=T.COMMAND_ALL.value)

args = parser.parse_args()

if args.command == C.COMMAND_SERVER.value:
    get_server_names()

elif args.command == C.COMMAND_AUCTIONS.value:
    get_auctions_data()

elif args.command == C.COMMAND_ITEMS.value:
    get_item_data()

elif args.command == C.COMMAND_ITEMS_CLASS.value:
    get_class_item_ids()

elif args.command == C.COMMAND_CHECK_AUCTION.value:
    check_items()

elif args.command == C.COMMAND_GET_MEDIA.value:
    get_items_media()

elif args.command == C.COMMAND_MK_DEAD_SERVERS.value:
    mark_dead_servers()

elif args.command == C.COMMAND_RM_SUS_TRANS.value:
    remove_suspiscious_transaction()

elif args.command == C.COMMAND_ALL.value:
    print("Executing all methods")
    methods = [get_server_names, get_auctions_data, get_item_data, get_class_item_ids, check_items, get_items_media,
               mark_dead_servers, remove_suspiscious_transaction]
    [m() for m in methods]
    print("Finished executing all methods.")

else:
    print(f"There is no such command for {args}")
