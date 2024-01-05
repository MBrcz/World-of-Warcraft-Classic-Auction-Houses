from enum import Enum


class EnumGetter(Enum):
    """
    This class holds only one method, it shall be passed to the child classes.
    :return: None
    """

    @classmethod
    def get_all_headers(cls) -> list[str]:
        """
        Returns all headers that are bound to the Auction Enum object.

        :return: list[str]
        """

        return [header.value for header in cls]


class Realms(EnumGetter):
    """
    This object is bound to the file Realms.csv, see more: Paths enum
    """

    REGION_ID = "Region ID"
    REALM_ID = "Realm ID"
    REALM_NAME = "Realms Name"
    IS_REALM_DEAD = "Is Realm Dead"


class Auctions(EnumGetter):
    """
    This object is bound to the file Auctions.csv, see more: Paths enum
    """

    REGION_ID = "Region ID"
    REALM_ID = "Realm ID"
    AUCTION_ID = "Auction ID"
    BID = "Bid"
    BUYOUT = "Buyout"
    QUANTITY = "Quantity"
    TIME_LEFT_ID = "Time Left ID"
    ITEM_ID = "Item ID"


class AuctionTimeLeft(EnumGetter):
    """
    This enum object holds all column names that are related to Auction Time Left.
    """

    TIME_LEFT_ID = "Time Left ID",
    TIME_LEFT_VALUE = "Time Left Value"


class Items(EnumGetter):
    """
    This enum object holds name of all properties of item objects.
    """

    ITEM_ID = "Item ID"
    ITEM_NAME = "Item Name"
    QUALITY_TYPE = "Quality Type"
    ITEM_LEVEL = "Item Level"
    ITEM_REQUIREMENT_LEVEL = "Item Requirement Level"
    # MEDIA = "MEDIA"
    ITEM_CLASS = "Item Class ID"
    ITEM_SUBCLASS = "Item Subclass ID"
    INVENTORY_TYPE_NAME = "Inventory Type Name"
#     ITEM_PURCHASE_PRICE = "Item Purchase Price"
#     ITEM_SELL_PRICE = "Item Sell Price"
    IS_STACKABLE = "Is stackable"
    IS_EQUIPABLE = "Is equipable"


class ItemsClassId(EnumGetter):
    """
    This enum object holds all data related to the headers of the file that holds info about items classes.
    """

    CLASS_NAME = "Item Class Name"
    CLASS_ID = "Item Class ID"
    SUBCLASS_NAME = "Item Subclass Name"
    SUBCLASS_ID = "Item Subclass ID"


class ItemsMedia(EnumGetter):
    """
    This enum object holds all data related to file containing the icons of the items.
    """

    ITEM_ID = "Item ID"
    MEDIA_URL = "Media URL"
