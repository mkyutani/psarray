#!/usr/bin/env python3

import sys
from PSArray import PSArray

def exec(cmd):
    print(">>>>>>>> {}".format(cmd))
    array = PSArray().build(cmd)
    print("<<<<<<<< {}".format(array))
    sep = "-" * 72
    counter = 0
    for dic in array:
        print(sep)
        for key, value in dic.items():
            print("{}: {}: [{}]".format(counter, key, value))
        counter = counter + 1

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

    # Some examples
    exec("get-service")
    exec("get-item (\"HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*\", \"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*\", \"HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*\") |%{ $k = $_; $k.getvalue(\"UninstallString\") |% { if ($_ -ne $null) { [pscustomobject]@{ key = $k.pspath; name = $k.getvalue(\"DisplayName\"); version = $k.getvalue(\"DisplayVersion\"); publisher = $k.getvalue(\"Publisher\"); uninstall = $_ }}}}")
    exec("get-process |%{ $p = $_; $x = $_.id; get-ciminstance -classname Win32_Process -namespace root\\cimv2 -filter \"processid = $x\" |%{ $u = (invoke-cimmethod -inputobject $_ -methodname getowner); [pscustomobject]@{ id = $p.id; processname = $p.processname; domain = $u.domain; user = $u.user; path = $_.executablepath; cmd = $_.commandline; priority = $_.priority; product = $p.product; productversion = $p.productversion; company = $p.company; description = $p.description }}}")
