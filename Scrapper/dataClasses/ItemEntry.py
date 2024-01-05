
"""This dataclass should contain data about items that are stored in Blizzard API."""


class ItemEntry:
    def __init__(self, json_content: dict) -> None:
        """
        Constructor for ItemEntry object. Stores the data of the item object.

        :param json_content: the content to be scrapped.
        """

        self._item_id: int = json_content['id']
        self._item_name: str = json_content['name']
        self._quality_type: str = json_content['quality']['name']
        self._item_level: str = json_content['level']
        self._item_required_level: str = json_content['required_level']
        # self._media_id: str = json_content['media']['id']
        self._item_class_id: str = json_content['item_class']['id']
        self._item_subclass_id: str = f"{self._item_class_id}_{json_content['item_subclass']['id']}"
        self._inventory_type_name: str = json_content['inventory_type']['name']
#         self._item_purchase_price: str = json_content['purchase_price']
#         self._item_sell_price: str = json_content['sell_price']
        self._is_item_equipalbe: str = json_content['is_equippable']
        self._is_item_stackable: str = json_content['is_stackable']

    def read_the_entries(self) -> list[str]:
        """
        This method returns the value of the stored text of the item object.

        :return: list[str]
        """

        return [
            self._item_id,
            self._item_name,
            self._quality_type,
            self._item_level,
            self._item_required_level,
#             self._media_id,
            self._item_class_id,
            self._item_subclass_id,
            self._inventory_type_name,
            # self._item_purchase_price,
            # self._item_sell_price,
            self._is_item_stackable,
            self._is_item_equipalbe
        ]