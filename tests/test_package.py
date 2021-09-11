import logging
import unittest

import package

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s [%(levelname)s]: %(message)s")


class PackageTest(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.logger.error("Setup Done")

    def test_importing(self):
        self.assertIsNotNone(package)
