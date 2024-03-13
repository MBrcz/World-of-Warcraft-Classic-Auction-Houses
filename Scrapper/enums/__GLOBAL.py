from enum import Enum
from os import cpu_count
"""
This file stores the fundamental constants related to the workings of application.
"""


class GLOBAL(Enum):

    CLIENT_ID: str = "" # The client id that will be used in order to get access to API.
    CLIENT_SECRET: str = "" # The client secret that will be used in order to get access to API.
    COUNT_USE_THREADS = cpu_count() # How many threads from user computer will be used in some functions.
                                    # By default is every possible.
    REGIONS = {1: "us", 2: "eu", 3: "kr", 4: "tw"}  # the regions from which the data shall be taken.
    K_FACTOR = 1.25
    QUARTILE_RANGE = 0.25
