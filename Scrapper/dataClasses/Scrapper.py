# Downloaded Libraries
from requests import post, get

# In-built Libraries
import re

"""
This module holds scrapper dedicated to use against Blizzard Vanilla API.
See more: https://develop.battle.net/documentation/world-of-warcraft-classic/game-data-apis
"""


class Scrapper:
    """
    This static class holds all methods and parameters that are related for getting the data from Blizzard API.
    """
    
    _CLIENT_ID: str = "PLACE YOUR CLIENT ID HERRE"
    _CLIENT_SECRET: str = "PLACE YOUR CLIENT SECRET HERE"

    ACCESS_TOKEN: str = None  # VARIABLE TO CHANGE, unique to the user
    NAMESPACE: str = None
    BASE_URL: str = "https://eu.api.blizzard.com/data/"
    LANGUAGE = "en_US"

    @classmethod
    def create_access_token(cls, region: str='us', namespace_type: str = 'static') -> dict:
        """
        This method allows to create for blizzard API unique access token.
        Also sets class attributes for object.
        DOES NOT WORK ON CHINEASE (of course under condition they exist), cuz dunno how Netease incident had finished!

        :param region: the region from which data is gathered. See more: Blizzard API docs.
        :param namespace_type: static or dynamic, depends on API settings (see more in API docs)
        :return: dictionary (response)
        """

        assert cls._CLIENT_ID != "" and cls._CLIENT_SECRET != ""
        assert namespace_type == 'static' or namespace_type == 'dynamic'

        data = {'grant_type': 'client_credentials'}
        if region == "tw":
            response = post('https://%s.battle.net/oauth/token' % "eu", data=data, auth=(cls._CLIENT_ID, cls._CLIENT_SECRET))
        else:
            response = post('https://%s.battle.net/oauth/token' % region, data=data, auth=(cls._CLIENT_ID, cls._CLIENT_SECRET))

        cls.ACCESS_TOKEN = response.json()['access_token']
        cls.BASE_URL = f"https://{region}.api.blizzard.com/data/"
        cls.NAMESPACE = f"{namespace_type}-classic1x-{region}"

        print(f"Access Token has been set for {region} and {namespace_type}.")
        return response.json()

    @classmethod
    def get_all_realm_ids(cls) -> list[int]:
        """
        This classmethod gets all realm ids out of the warcraft API

        :return: Numbers of all ids got from the API.
        """

        url: str = f"{cls.BASE_URL}wow/connected-realm/index"
        content = cls.open_blizzard_api_website(url)

        result: list[int] = []
        for realm in content['connected_realms']:
            result.append(int(re.findall(r'\d+', realm['href'])[0]))
        return result

    @classmethod
    def get_realm_content(cls, realm_id: int) -> dict:
        """
        Gets realm content out of knowing the realm id object.

        :param realm_id: id of the realm from which the data will be gathered
        :return: dict (json response)
        """

        url: str = f"{cls.BASE_URL}wow/connected-realm/{realm_id}"
        realm_content = cls.open_blizzard_api_website(url)
        return realm_content

    @classmethod
    def get_auction_data(cls, realm_id: int) -> dict:
        """
        Gets the auction data from Blizzard api.

        :param realm_id: id of the realm from which the data will be gathered
        :return: dict (json response)
        """

        url: str = f"{cls.BASE_URL}wow/connected-realm/{realm_id}/auctions/index"
        auction_data = cls.open_blizzard_api_website(url)
        return auction_data

    @classmethod
    def get_item_data(cls, item_id: int) -> dict:
        """
        This method gets item data from the website.

        :param item_id: The id of the item that will be searched.
        :return: Dictionary
        """

        url = f'{cls.BASE_URL}wow/item/{item_id}'
        item_data = cls.open_blizzard_api_website(url)
        return item_data

    @classmethod
    def get_item_class_data(cls, class_id: int) -> dict:
        """Gets the description of classes from the website

        :param class_id: id of the class that will be tested
        :return Dictionary
        """

        url: str = f'{cls.BASE_URL}wow/item-class/{class_id}'
        item_class_data = cls.open_blizzard_api_website(url)
        return item_class_data

    @classmethod
    def get_item_media_info(cls, item_id: int) -> dict:
        """
        Gets the url to the item icon from website.

        :param item_id: The id of the searched item
        :return: dict
        """

        url: str = f"{cls.BASE_URL}wow/media/item/{item_id}"
        item_media_data = cls.open_blizzard_api_website(url)
        return item_media_data

    @classmethod
    def open_blizzard_api_website(cls, url: str) -> dict:
        """
        This method primary goal is to open the API site of the vanilla Blizzard Api.
        USE ONLY BARE URLS HERE, in another case it won't work!

        :argument url: link to the page that you wanna open
        :return requests (in json format)
        """

        if f"?namespace={cls.NAMESPACE}" in url:
            url = url.replace(f"?namespace={cls.NAMESPACE}", "")

        url = url + f"?namespace={cls.NAMESPACE}&locale={cls.LANGUAGE}&access_token={cls.ACCESS_TOKEN}"

        request = get(url)
        status_code: int = request.status_code

        if status_code == 200:
            return request.json()
        else:
            print(f"Cannot connect to {url}. Error num: {status_code}")
