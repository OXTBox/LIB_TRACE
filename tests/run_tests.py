#!/usr/bin/env python3
"""Run LIB_TRACE's tests inside real LiveCode 9.6.3, through LIB_MCP's standalone server.

    python3 tests/run_tests.py

Loads livecode/lib_trace.livecodescript into the standalone with `start using`, evaluates
each expression there and compares with the expected text. Needs ~/projects/LIB_MCP.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(os.path.dirname(HERE), 'livecode', 'lib_trace.livecodescript')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'LIB_MCP', 'python'))
from lib_mcp.client import Client, local_to_win

def grid(*rows):
    return ' & return & '.join('"%s"' % r for r in rows)

TESTS = [
    ('Trace.Contours(%s)' % grid('000', '010', '000'), '2,2'),
    ('Trace.Contours(%s)' % grid('0000', '0110', '0110', '0000'), '2,2\n3,2\n3,3\n2,3\n2,2'),
    ('Trace.Contours(%s)' % grid('111', '111', '111'), '1,1\n2,1\n3,1\n3,2\n3,3\n2,3\n1,3\n1,2\n1,1'),
    ('Trace.Contours(%s)' % grid('11111', '10001', '10001', '11111'),
     '1,1\n2,1\n3,1\n4,1\n5,1\n5,2\n5,3\n5,4\n4,4\n3,4\n2,4\n1,4\n1,3\n1,2\n1,1'),
    ('Trace.Contours(%s)' % grid('110011', '110011'), '1,1\n2,1\n2,2\n1,2\n1,1\n\n5,1\n6,1\n6,2\n5,2\n5,1'),
    ('Trace.Contours(%s)' % grid('000', '000'), ''),
    ('Trace.MaskToGrid(numToByte(0) & numToByte(255) & numToByte(255) & numToByte(0), 2, 2)', '01\n10'),
    ('Trace.Offset("1,1" & return & return & "2,3", 10, 20)', '11,21\n\n12,23'),
    ('Trace.Scale("1,1" & return & return & "2,3", 8)', '8,8\n\n16,24'),
]


def main():
    c = Client.standalone()
    # a stack stays in memory after "stop using"; delete it so the file is read again
    ok, out = c.run('if there is a stack "LIB_TRACE" then delete stack "LIB_TRACE"\n'
                    'start using stack "%s"\nput "loaded"' % local_to_win(LIB).replace('\\', '/'), in_server=True)
    if not ok or 'loaded' not in out:
        print('Could not load LIB_TRACE:', out)
        return 2
    failed = 0
    for expr, want in TESTS:
        ok, got = c.eval(expr, in_server=True)
        got = got.replace('\r', '')
        good = ok and got == want
        failed += not good
        print('%s  %s' % ('PASS' if good else 'FAIL', expr if good else '%s\n      want %r\n      got  %r' % (expr, want, got)))
    c.run('stop using stack "%s"' % local_to_win(LIB).replace('\\', '/'), in_server=True)
    print('\n%d of %d passed' % (len(TESTS) - failed, len(TESTS)))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
