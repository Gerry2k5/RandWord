#!/usr/bin/env python3

import timeit

REPS=1000


no_mmap = timeit.Timer(stmt='get_affix_rules("/usr/share/myspell/dicts/en_GB-large.aff")', setup='from randword import get_affix_rules')
with_mmap = timeit.Timer(stmt='get_affix_rules2("/usr/share/myspell/dicts/en_GB-large.aff")', setup='from randword import get_affix_rules2')

print("Without MMAP, {} repetitions took {} seconds".format(REPS, no_mmap.timeit(REPS)))
print("With MMAP, {} repetitions took {} seconds".format(REPS, with_mmap.timeit(REPS)))
