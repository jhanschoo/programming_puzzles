import sys
from . import solve

with open(sys.argv[1]) as f:
    print(solve(f))
