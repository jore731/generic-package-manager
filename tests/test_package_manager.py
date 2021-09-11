import filecmp
import logging
import unittest

import package_manager
import os

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s [%(levelname)s]: %(message)s")


class PackageManagerTest(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.logger.error("Setup Done")

    def test_importing(self):
        print(os.system('../package_manager.py -f input.txt -o output.txt'))
        self.assertTrue(filecmp.cmp('output.txt','output_reference.txt'))

