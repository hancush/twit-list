import pprint

from topper_class import Sample, Rank
from config import *

go = Rank()

answer = int(raw_input("""1 - Rank by volume
2 - Rank by time period
> """))

if answer == 1:
    go.rank_vol(raw_input("""How many tweets would you like to rank?
> """))
else:
    go.rank_per(int(raw_input("""How many hours' worth of tweets would you like to rank?
> """)))
