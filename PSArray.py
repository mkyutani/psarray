#!/usr/bin/env python3

import chardet
import io
import platform
import subprocess
from subprocess import PIPE, DEVNULL

class PSArray:

    def __init__(self):
        self.stream = None
        self.nextline = None

    def readline(self):
        if self.stream is None:
            return None
        if self.nextline is None:
            current = self.stream.readline()
            if current is None:
                return None
        else:
            current = self.nextline
        line = self.stream.readline()
        while line is not None and len(line) > 0 and line[0] == " ":
            current = current.rstrip() + line.lstrip()
            line = self.stream.readline()
        self.nextline = line
        return current

    def build(self, cmd):
        self.stream = None
        self.nextline = None

        cmd = cmd + "| format-list *"
        if platform.system() != "Windows":
            cmd = cmd.replace("\\", "\\\\")
            cmd = cmd.replace("$", "\$")
        cmd = cmd.replace("\"", "\\\"")
        cmd = "powershell.exe -command \"& {" + cmd + "}\""

        proc = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=DEVNULL)
        out, err = proc.communicate()

        if len(out) > 0:
            coding = chardet.detect(out)["encoding"]
            if coding is not None:
                self.stream = io.StringIO(out.decode(coding))

        all_list = []
        item_alist = {}
        line = self.readline()
        while line:
            line = line.strip()
            if len(line) > 0:
                name, value = line.split(':', 1)
                name = name.strip()
                value = value.strip()
                item_alist.update({name: value})
            else:
                if len(item_alist) > 0:
                    all_list.append(item_alist)
                    item_alist = {}
            line = self.readline()

        if len(item_alist) > 0:
            all_list.append(item_alist)
            item_alist = {}

        return all_list

if __name__ == "__main__":

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

