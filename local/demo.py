from topper_local import Rank, get_lists
from config import *

which = get_lists('hancush')

go = Rank(which)

go.rank_per(12)
