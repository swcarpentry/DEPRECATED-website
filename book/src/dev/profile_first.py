import cProfile, pstats
from invperc import main

cProfile.run('main("random", ["51", "100", "127391"])', 'list.prof')
p = pstats.Stats('list.prof')
p.strip_dirs().sort_stats('time').print_stats()
