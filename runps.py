#!/usr/bin/env python3

import sys
from tabulate import tabulate
from PSArray import PSArray

isFirst = True
def exec(cmd):
    global isFirst
    if isFirst:
        isFirst = False
    else:
        print('='*72)
    print(cmd)
    array = PSArray().build(cmd)
    if len(array) == 0:
        print('(empty)')
    else:
        print(tabulate(array, headers='keys', showindex=True))

if len(sys.argv) >= 2:
    for c in sys.argv[1:]:
        exec(c)
else:
    # Command must be a Powershell script which returns an object list as an expression
    # NG -> not an object list but an array
    exec("foreach ($i in \"foo\", \"bar\", \"baz\") { $i[0], $i.substring(1) }")
    # NG -> context is not expression but sentence
    exec("foreach ($i in \"foo\", \"bar\", \"baz\") { [pscustomobject]@{ car = $i[0]; cdr = $i.substring(1) }}")
    # OK -> variable is an expression
    exec("$o = foreach ($i in \"foo\", \"bar\", \"baz\") { [pscustomobject]@{ car = $i[0]; cdr = $i.substring(1) }}; $o")
    # OK -> return value of invoked script block is an expression
    exec("(.{foreach ($i in \"foo\", \"bar\", \"baz\") { [pscustomobject]@{ car = $i[0]; cdr = $i.substring(1) }}})")

    # Sample: Win32 Services
    exec("get-service")

