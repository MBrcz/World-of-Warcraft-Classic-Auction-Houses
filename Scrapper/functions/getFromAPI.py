# Python Libraries
import pandas as pd
from os.path import join, exists
from os import listdir
from threading import Thread
from gc import collect
from numpy import array_split, vstack
from time import sleep
from random import uniform

# User Defined Libraries
from enums.__GLOBAL import GLOBAL
from enums.Paths import Paths
from enums import Headers
from dataClasses.Scrapper import Scrapper
from dataClasses.ItemEntry import ItemEntry
from dataClasses.ItemIdEntry import ItemIdEntry
from dataClasses.ItemMediaEntry import ItemMediaEntry


"""
THIS CODE WORKS ONLY ON BLIZZARD VANILLA CLASSIC API - 07.11.2023
It holds all major functions used in the project related to gathering data.
"""

_REGIONS = GLOBAL.REGIONS.value


def create_table_of_valid_realms() -> None:
    """
    Downloads the table of the valid realms from blizzard API.
    The result should look like this:
    {"Region Id", "Realm Id", "Realm Name"}

    :return: csv file called realms
    """

    content_to_save = {
        Headers.Realms.REGION_ID.value: [],
        Headers.Realms.REALM_ID.value: [],
        Headers.Realms.REALM_NAME.value: []
    }

    for region_id, region_name in _REGIONS.items():
        Scrapper.create_access_token(region_name, namespace_type='dynamic')
        all_realms_ids = Scrapper.get_all_realm_ids()

        for count, realm_id in enumerate(all_realms_ids):
            realm = Scrapper.get_realm_content(realm_id)
            if realm is None:
                print(f"It seems that realm with id {realm_id} {region_name} does not exist.")
                continue

            content_to_save[Headers.Realms.REGION_ID.value].append(region_id)
            content_to_save[Headers.Realms.REALM_ID.value].append(realm_id)
            content_to_save[Headers.Realms.REALM_NAME.value].append(realm['realms'][0]['name'])

    df = pd.DataFrame(content_to_save)
    df.to_csv(Paths.REALMS.value, index=False, index_label=False)


def download_auction_data_from_web() -> None:
    """
    Downloads the auction house data from the blizzard API by all regions.

    :return: None
    """

    def format_auction_dataframe_columns(auction_dataframe: pd.DataFrame):
        """
        This helper method formats the columns of the new added dataframe column
        :return: pd.Dataframe
        """

        auction_dataframe[Headers.Auctions.REALM_ID.value] = row_realm_id
        auction_dataframe[Headers.Auctions.REGION_ID.value] = row_region_id
        auction_dataframe[Headers.Auctions.AUCTION_ID.value] = auction_id

        auction_dataframe.rename(columns=
                                 {
                                     "item.id": Headers.Auctions.ITEM_ID.value,
                                     "bid": Headers.Auctions.BID.value,
                                     "buyout": Headers.Auctions.BUYOUT.value,
                                     "quantity": Headers.Auctions.QUANTITY.value,
                                     "time_left": Headers.Auctions.TIME_LEFT_ID.value
                                 }, inplace=True)

        # Gets rid of all other (non changed) columns.
        for column in auction_dataframe.columns:
            if column not in Headers.Auctions.get_all_headers():
                auction_dataframe.drop(columns=column, inplace=True)

        return auction_dataframe

    def switch_time_left_for_integers(auction_dataframe) -> pd.DataFrame:
        """In order to save some additional space, it is necessary to change the time_left into numbers.

        :param: auction_dataframe - the dataframe that will be converted
        :return: modified dataframe.
        """
        """Made by Chatgpt."""

        auction_time_table = pd.read_csv(Paths.AUCTIONS_TIME_LEFT.value)
        time_left_id = Headers.Auctions.TIME_LEFT_ID.value

        # Create a mapping dictionary from the time_left_table
        mapping_dict = dict(
            zip(auction_time_table[Headers.AuctionTimeLeft.TIME_LEFT_VALUE.value], auction_time_table[time_left_id]))

        # Use the map function to replace values
        auction_dataframe[time_left_id] = auction_dataframe[time_left_id].map(mapping_dict)

        return auction_dataframe

    realms = pd.read_csv(Paths.REALMS.value)
    current_region_id: int = 0

    auction_data: None | pd.DataFrame = None
    for index, row in realms.iterrows():
        row = row.to_dict()
        row_region_id: int = row[Headers.Realms.REGION_ID.value]
        row_realm_id: int = row[Headers.Realms.REALM_ID.value]

        if row_region_id != current_region_id:
            current_region_id = row_region_id
            Scrapper.create_access_token(
                region=_REGIONS[current_region_id],
                namespace_type="dynamic")

        auctions_in_realm: dict = Scrapper.get_auction_data(row_realm_id)

        for count, auction in enumerate(auctions_in_realm['auctions']):
            auction_id: int = auction['id']
            retry_loop: bool = False

            # This while loop is a solution for BadGateway error, which for some unknown reason happens.
            # This error happens only using call.py all method.
            while not retry_loop:
                try:
                    auction_content = Scrapper.open_blizzard_api_website(auction['key']['href'])
                    auction_content = auction_content['auctions']
                    df = pd.json_normalize(data=auction_content)
                    df = format_auction_dataframe_columns(df)

                    if auction_data is None:
                        auction_data = df

                    else:
                        auction_data = pd.concat([auction_data, df])
                    break

                except KeyError:
                    print(f"It looks like in region {_REGIONS[current_region_id]} realm: "
                          f"{row_realm_id} there is no content in {auction['name']}")
                    break

                except TypeError:
                    print("--------- BAD GATEWAY ERROR -------------")
                    print(f"Current auction and realm: {auction}, {row_realm_id}")

        print(auction_data)
    auction_data = switch_time_left_for_integers(auction_data)
    auction_data.to_csv(Paths.AUCTIONS.value, index_label=False, index=False)


def download_items_data_from_web() -> None:
    """
    This method downlaods all data items that has been shown in the auction house from blizzard API.
    It uses multithreading with quantity of maximum possible threads at the same time.

    :return: None
    """

    def get_data_from_api(sub_id_items: list[int], thread_num: int) -> None:
        """
        Function that performs the scrapping operation on the items.

        :param sub_id_items: The list of items that will be scrapped in the particular thread.
        :param thread_num: The number of the thread (for debugging purposes)
        :return: None
        """

        for count, item_id in enumerate(sub_id_items):
            content = Scrapper.get_item_data(item_id)
            try:
                items.append(ItemEntry(content))
                print(f"Thread: {thread_num} - item {item_id} has been scrapped, there are left to scrap only: {len(sub_id_items) - count}")
                sleep(uniform(0.3, 1.2))
            except TypeError:
                print("Type Err!")

    threads_active: int = GLOBAL.COUNT_USE_THREADS.value
    items: list[ItemEntry] = []
    Scrapper.create_access_token(namespace_type='static')
    unique_items = list(pd.read_csv(Paths.AUCTIONS.value)[Headers.Auctions.ITEM_ID.value].unique())

    global_count = 0
    main_df: None | pd.DataFrame = None
    while global_count <= len(unique_items):
        threads: list[Thread] = []
        list_ids = array_split(unique_items[global_count: global_count + 100], threads_active)

        for count, ids in enumerate(list_ids):
            new_thread = Thread(target=get_data_from_api, args=(ids, count))
            threads.append(new_thread)
            threads[-1].start()

        for thread in threads:
            thread.join()

        df = pd.DataFrame(columns=Headers.Items.get_all_headers(), data=[it.read_the_entries() for it in items])
        if main_df is None:
            main_df = df
        else:
            main_df = pd.concat([main_df, df])

        global_count += 100
        print(f"GLOBAL COUNT: {global_count}")

    main_df.drop_duplicates(inplace=True)
    main_df.to_csv(Paths.ITEMS.value, index_label=False, index=False)


def download_class_and_subclass_descriptions_from_web() -> None:
    """
    Finds the description of item classes and subclasses from blizzard API.
    WARNING! In order this function to work, it is necessary for download_items_data_from_web function to be executed!

    :return: None
    """

    item_file_path: str = Paths.ITEMS.value

    if not exists(item_file_path):
        raise FileNotFoundError(f"Cannot execute code to the fact that {item_file_path} does not exist!")

    item_frame: pd.DataFrame = pd.read_csv(item_file_path)
    class_ids = sorted(list(item_frame[Headers.Items.ITEM_CLASS.value].unique()))

    Scrapper.create_access_token(namespace_type='static')

    class_subclass_list: list[ItemIdEntry] = []  # variable that will hold the class data from API
    for count, class_id in enumerate(class_ids):
        data_from_web: dict = Scrapper.get_item_class_data(class_id)

        for subclass in data_from_web['item_subclasses']:
            class_subclass_list.append(ItemIdEntry(data_from_web))
            class_subclass_list[-1].add_subclasses(subclass)
            print(f"Added: {class_subclass_list[-1].read_the_entries()}")

    df = pd.DataFrame(columns=Headers.ItemsClassId.get_all_headers(), data=[v.read_the_entries() for v in class_subclass_list])
    df.to_csv(Paths.ITEMS_CLASSES.value, index_label=False, index=False)


# Yea, this function is really similar to download_items_data_from_web().
def download_item_media_description_from_web() -> None:
    """
    Downloads the data about media (icons of items) from Blizzard API website.
    WARNING! In order this function to work, it is necessary for download_items_data_from_web function to be executed!

    :return: None
    """

    def get_data_from_api(sub_id_items: list[int], thread_num: int) -> None:
        """
        Function that performs the scrapping operation on the items.

        :param sub_id_items: The list of items that will be scrapped in the particular thread.
        :param thread_num: The number of the thread (for debugging purposes)
        :return: None
        """

        for count, item_id in enumerate(sub_id_items):
            content = Scrapper.get_item_media_info(item_id)
            try:
                class_item_ids.append(ItemMediaEntry(content))
                print(f"Thread: {thread_num} - item {item_id} has been scrapped, there are left to scrap only: {len(sub_id_items) - count}")
                sleep(uniform(0.3, 1.2))
            except TypeError:
                print("Type Err!")

    item_path_file: str = Paths.ITEMS.value
    if not exists(item_path_file):
        raise FileNotFoundError(f"Cannot execute code to the fact that {item_path_file} does not exist!")

    item_frame: pd.DataFrame = pd.read_csv(item_path_file)
    item_ids: list[int] = sorted(list(item_frame[Headers.Items.ITEM_ID.value].unique()))

    Scrapper.create_access_token(namespace_type='static')

    class_item_ids: list[ItemMediaEntry] = []
    threads_active = GLOBAL.COUNT_USE_THREADS.value

    global_count: int = 0
    main_df: None | pd.DataFrame = None
    while global_count <= len(item_ids):
        threads = []
        list_ids = array_split(item_ids[global_count: global_count + 100], threads_active)

        for count, ids in enumerate(list_ids):
            new_thread = Thread(target=get_data_from_api, args=(ids, count))
            threads.append(new_thread)
            threads[-1].start()

        for thread in threads:
            thread.join()

        df = pd.DataFrame(columns=Headers.ItemsMedia.get_all_headers(), data=[it.read_the_entries() for it in class_item_ids])
        if main_df is None:
            main_df = df
        else:
            main_df = pd.concat([main_df, df])

        global_count += 100
        print(f"GLOBAL COUNT: {global_count}")

    main_df.drop_duplicates(inplace=True)
    main_df.to_csv(Paths.ITEMS_ICONS_URL.value, index_label=False, index=False)
