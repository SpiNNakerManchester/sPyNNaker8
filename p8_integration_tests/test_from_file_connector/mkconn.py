"""
A simple script to generate connection data for
test_from_file_connector_large.py.
"""

import os
import random
import numpy

connection_list = []
for i in range(255):
    connection_list.append(
        (i, random.randint(0, 255), random.random(), random.randint(10, 15)))

current_file_path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_file_path, "large.connections")
if os.path.exists(path):
    os.remove(path)

numpy.savetxt(path, connection_list)
