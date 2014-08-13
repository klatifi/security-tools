#!/usr/bin/python

import sys

#------------------------------------------------------------------------------
# Main Program
#------------------------------------------------------------------------------
patterns = ['flast', 'firstl', 'first.last']

if len(sys.argv) != 4:
    print 'Usage: usernames.py firsts lasts pattern'
    print 'Valid patterns include {0}'.format(', '.join(patterns))
    sys.exit()

p = sys.argv[3]

if p not in patterns:
    print 'Pattern must be one of {0}'.format(', '.join(patterns))
    sys.exit()

for last in open(sys.argv[2]):
    last = last.rstrip('\r\n')
    for first in open(sys.argv[1]):
        first = first.rstrip('\r\n')
        if p == 'flast':
            print '{0}{1}'.format(first[0], last)
        if p == 'firstl':
            print '{0}{1}'.format(first, last[0])
        if p == 'first.last':
            print '{0}.{1}'.format(first, last)
