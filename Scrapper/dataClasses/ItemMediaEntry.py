"""
This file shall contains data about the file that stores entries about item medias.
"""


class ItemMediaEntry:
    def __init__(self, json_object: dict):
        """
        Constructor for ItemMediaEntry Object.

        :param json_object: the content that is a response from blizzard API.
        """
        self._item_id = json_object['id']
        self._item_media_url = json_object['assets'][0]['value']

    def read_the_entries(self) -> list[str]:
        """
        Returns all atrributes as list of string

        :return: list[str]
        """

        return [
            self._item_id,
            self._item_media_url
        ]