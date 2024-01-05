from enum import Enum
from os import cpu_count
"""
This file stores the fundamental constant related to the workings of application.
"""


class GLOBAL(Enum):

    COUNT_USE_THREADS = cpu_count() # How many threads from user computer will be used in some functions.
                                    # By default is every possible.
    REGIONS = {1: "us", 2: "eu", 3: "kr", 4: "tw"}  # the regions from which the data shall be taken.
    K_FACTOR = 1.25
    QUARTILE_RANGE = 0.25
