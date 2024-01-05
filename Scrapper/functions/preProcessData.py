# # In-built imports
import pandas as pd
import numpy as np
from os.path import exists
from threading import Thread

# # User imports
from enums.__GLOBAL import GLOBAL
from enums.Paths import Paths
from enums.Headers import Auctions, Realms, Items

"""
This module checks if the data downloaded from api is definetelly correct.
"""


def check_items() -> None:
    """
    Checks if items from auction and items.csv contains the same items within.
    If so, terminates the unknown items from Auction.csv.

    :return None
    """

    assert exists(Paths.AUCTIONS.value) and exists(Paths.ITEMS.value)

    auctions_data = pd.read_csv(Paths.AUCTIONS.value)
    items_data = pd.read_csv(Paths.ITEMS.value)

    auctions_unique_items_id: list[int] = list(auctions_data[Auctions.ITEM_ID.value].unique())
    print(len(auctions_unique_items_id))
    print(len(items_data))
    items_unique_items_id: list[int] = list(items_data[Items.ITEM_ID.value].unique())

    invalid_items: list[int] = [item for item in auctions_unique_items_id if item not in items_unique_items_id]

    if auctions_unique_items_id == items_unique_items_id:
        print("The item ids from auction and items are the same.")

    else:
        print(f"The data from auction and items are not the same! Invalid items are: {invalid_items}!\n"
              f"Removing them from auction house...")

        cleared_auctions_data = auctions_data.loc[~auctions_data[Auctions.ITEM_ID.value].isin(invalid_items)]
        cleared_auctions_data.to_csv(Paths.AUCTIONS.value, index_label=False, index=False)
        print(f"Operation finished. Terminated {len(auctions_data) - len(cleared_auctions_data)} entries.")


# Yes this might be as well made from Power Query Editor.
def mark_dead_servers():
    """
    Marks the servers that are considered to be dead from the auction data file.
    Might be really handy in analysis.
    The server is considered to be dead, when it has less than 1000 quantities of transactions with it.

    :return: None
    """

    _MARK_DEAD_THRESHOLD: int = 1000
    assert exists(Paths.AUCTIONS.value) and exists(Paths.REALMS.value)

    print("... Marking Dead servers ...")
    realms_names: pd.DataFrame = pd.read_csv(Paths.REALMS.value)
    auctions_data: pd.DataFrame = pd.read_csv(Paths.AUCTIONS.value)

    realms_id = realms_names[[Realms.REALM_ID.value, Realms.REGION_ID.value]]

    # Loops through all realms and regions
    is_dead_flag: list[bool] = []
    for index, row in realms_id.iterrows():
        region_id, realm_id = row[Realms.REGION_ID.value], row[Realms.REALM_ID.value]
        filtered_auctions = auctions_data.loc[
            (auctions_data[Auctions.REGION_ID.value] == region_id) &
            (auctions_data[Auctions.REALM_ID.value] == realm_id)
            ]

        if len(filtered_auctions) < _MARK_DEAD_THRESHOLD:
            is_dead_flag.append(True)
        else:
            is_dead_flag.append(False)

    realms_names[Realms.IS_REALM_DEAD.value] = is_dead_flag
    realms_names.to_csv(Paths.REALMS.value, index=False, index_label=False)
    print(f"Found total {len([flag for flag in is_dead_flag if flag])} dead servers.")


def remove_suspicious_transactions() -> None:
    """
    This function is designed to remove the suspicious transaction from the auction house.csv.
    In other words, this method is designed to remove the outliers from auction.csv data set to make values look
    much better. In order to achieve that I will use the Interquartile Range (IQR) Method with k factor equal to 1.25.

    How does this exactly work:
    a) Removes every transaction that has buyout value == 0 (cuz it would destroy the lower quantile calculations).
    b) Forces every transaction to the value per quantity in auction file.
    c) Finds every server names and items
    d) Loops for all items in Auctions.csv
    e) Terminates all results that are not in a selected list.

    :return: None
    """

    def remove_outliers(array_of_items: np.ndarray, thread_num: int) -> None:
        """
        Method for removing the outliers in the current thread.

        :return: None
        """

        for count, item_num in enumerate(array_of_items):
            for row in unique_servers_regions.itertuples(index=False):
                reg_id, realm_id = row
                filtered_auction = auctions_data.loc[
                    (auctions_data[Auctions.REALM_ID.value] == realm_id) &
                    (auctions_data[Auctions.REGION_ID.value] == reg_id) &
                    (auctions_data[Auctions.ITEM_ID.value] == item_num)
                ]

                if len(filtered_auction) != 0:
                    lower: float = 0 + _QUARTILE_RANGE
                    upper: float = 1 - _QUARTILE_RANGE

                    quantiles: list[int] = filtered_auction[Auctions.BUYOUT.value].quantile(
                        [lower, upper]
                    )
                    difference = quantiles[upper] - quantiles[lower]  # NOQA
                    lower_bound: float = quantiles[lower] - _K_FACTOR * difference  # NOQA
                    upper_bound: float = quantiles[upper] + _K_FACTOR * difference  # NOQA

                    filtered_auction = filtered_auction.loc[
                        (filtered_auction[Auctions.BUYOUT.value] >= lower_bound) &
                        (filtered_auction[Auctions.BUYOUT.value] <= upper_bound)
                        ]

                    saved_items.extend(filtered_auction.index)

            print(f'Thread Num: {thread_num} has {len(saved_items)} elements. Analyzed {count} items of '
                  f'{len(array_of_items)}.')

    _K_FACTOR: int | float = GLOBAL.K_FACTOR.value
    _QUARTILE_RANGE: float = GLOBAL.QUARTILE_RANGE.value
    _THREADS_COUNT: int = GLOBAL.COUNT_USE_THREADS.value
    saved_items: list[str] = []

    assert exists(Paths.AUCTIONS.value) and exists(Paths.ITEMS.value) and exists(Paths.REALMS.value)
    print("...Removing outliners...")
    print("... THIS METHOD WILL LAST REALLY LONG ...")

    auctions_data: pd.DataFrame = pd.read_csv(Paths.AUCTIONS.value)
    auctions_data[Auctions.BUYOUT.value] = auctions_data[Auctions.BUYOUT.value].loc[
        auctions_data[Auctions.BUYOUT.value] != 0
    ]

    auctions_data[Auctions.BUYOUT.value] = auctions_data[Auctions.BUYOUT.value] / auctions_data[Auctions.QUANTITY.value]
    auctions_data = auctions_data[[Auctions.ITEM_ID.value, Auctions.BUYOUT.value, Auctions.REALM_ID.value, Auctions.REGION_ID.value]]

    items_data: pd.DataFrame = pd.read_csv(Paths.ITEMS.value)
    server_names: pd.DataFrame = pd.read_csv(Paths.REALMS.value)

    unique_items_id = items_data[Items.ITEM_ID.value]
    unique_servers_regions = server_names[[Realms.REGION_ID.value, Realms.REALM_ID.value]]

    split_items_id_list = np.array_split(unique_items_id.to_list(), _THREADS_COUNT)

    thread_list: list[Thread] = []
    for thread_count, list_num in enumerate(split_items_id_list):
        thread_list.append(Thread(target=remove_outliers, args=(list_num, thread_count)))
        thread_list[-1].start()

    for thread in thread_list:
        thread.join()

    auctions_data: pd.DataFrame = pd.read_csv(Paths.AUCTIONS.value)
    auctions_data = auctions_data[auctions_data.index.isin(saved_items)]
    auctions_data.to_csv(Paths.AUCTIONS.value, index=False, index_label=False)
