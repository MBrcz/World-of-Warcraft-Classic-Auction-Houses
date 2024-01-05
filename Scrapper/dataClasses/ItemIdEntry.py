"""
This file shall hold dataclass that is responsible for getting the parameters for getting the class descriptions from API
"""


class ItemIdEntry:
    def __init__(self, json_object: dict):
        """
        Constructor for ItemIdEntry Object.

        :param json_object: the data from WebApi to be scrapped from.
        """

        self._class_id = json_object['class_id']
        self._class_name = json_object["name"]
        self._subclass_id = None
        self._subclass_name = None

    def add_subclasses(self, subclasses_dict: dict) -> None:
        """
        Adds the data to the class about subclasses.

        :param subclasses_dict: The dictionary that stores data about the subclasses.
        :return: None
        """

        self._subclass_name = f'{subclasses_dict["name"]}'
        self._subclass_id = f'{self._class_id}_{subclasses_dict["id"]}'

    def read_the_entries(self) -> list[str]:
        """
        This method returns the value of the stored text of the item object.

        :return: list[str]
        """

        return [
            self._class_id,
            self._class_name,
            self._subclass_name,
            self._subclass_id
        ]
