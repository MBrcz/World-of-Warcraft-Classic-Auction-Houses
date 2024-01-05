from enum import Enum

"""This file shall store the name of the commands used in CML application."""


class CMLCommands(Enum):
    COMMAND = "command"
    COMMAND_SERVER = "servers"
    COMMAND_ITEMS = "items"
    COMMAND_AUCTIONS = "auctions"
    COMMAND_ITEMS_CLASS = "items_classes"
    COMMAND_GET_MEDIA = "items_media"

    COMMAND_CHECK_AUCTION = "check_auction_items"
    COMMAND_MK_DEAD_SERVERS = "mk_dead_servers"
    COMMAND_RM_SUS_TRANS = "rm_sus_trans"

    COMMAND_ALL = "all"
