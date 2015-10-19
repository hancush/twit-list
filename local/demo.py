import pprint

from topper_local import Rank, get_lists
from config import *

which = get_lists()
#which = 211727260

go = Rank(which)

go.rank_per(12)
