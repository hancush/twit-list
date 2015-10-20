from topper_local import Rank, get_lists, calls
from config import *

which = get_lists('hancush')

go = Rank(which)

print calls

go.rank_per(12)

print calls
