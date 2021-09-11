import logging
import unittest

import package_manager

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s [%(levelname)s]: %(message)s")


class PackageManagerTest(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.logger.error("Setup Done")

    def test_importing(self):
        self.assertIsNotNone(package_manager)
