#!/usr/bin/env python3
import sys
from pathlib import Path
import unittest
import itertools, re

sys.path.insert(0, str(Path(__file__).parent.parent))

from collections import OrderedDict

dict = OrderedDict

import antiflash
from antiflash import *


class Tests(unittest.TestCase):

	def testSimple(self):
		raise NotImplementedError


if __name__ == "__main__":
	unittest.main()
