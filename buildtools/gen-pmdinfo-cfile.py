#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2020 Dmitry Kozlyuk <dmitry.kozliuk@gmail.com>

import os
import subprocess
import sys
import tempfile
from security import safe_command

_, tmp_root, ar, archive, output, *pmdinfogen = sys.argv
with tempfile.TemporaryDirectory(dir=tmp_root) as temp:
    paths = []
    for name in safe_command.run(subprocess.run, [ar, "t", archive], stdout=subprocess.PIPE,
                               check=True).stdout.decode().splitlines():
        if os.path.exists(name):
            paths.append(name)
        else:
            safe_command.run(subprocess.run, [ar, "x", os.path.abspath(archive), name],
                           check=True, cwd=temp)
            paths.append(os.path.join(temp, name))
    safe_command.run(subprocess.run, pmdinfogen + paths + [output], check=True)
