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
