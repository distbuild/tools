#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

FILE_NAME = "test.txt"
SIZE_MB = 20
CHUNK_SIZE = 1024 * 1024

with open(FILE_NAME, 'wb') as f:
    for _ in range(SIZE_MB):
        f.write(os.urandom(CHUNK_SIZE))

print(f"Created file {FILE_NAME} of size {SIZE_MB}MB")
