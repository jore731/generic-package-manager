import logging
import unittest

import package

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s [%(levelname)s]: %(message)s")


def raise_exception():
    raise Exception


class PackageInstallingTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_importing(self):
        self.assertIsNotNone(package)

    def test_create_package(self):
        new_package = package.Package("nano")
        self.assertEqual(new_package.name, "nano")

    def test_install_package(self):
        new_package = package.Package("nano")
        new_package.install(True)
        self.assertTrue(new_package.installed)
        self.assertTrue(new_package.explicitly_installed)

    def test_package_not_installed(self):
        new_package = package.Package("nano")
        self.assertFalse(new_package.installed)

    def test_register_dependency(self):
        self.main_package = package.Package("main_package")
        self.dependency = package.Package("dependency")
        self.dependency2 = package.Package("dependency2")
        self.main_package.depends_on(self.dependency)
        self.main_package.depends_on(self.dependency2)
        self.assertEqual(self.main_package.dependencies[0].name, "dependency")

    def test_install_package_with_dependencies(self):
        self.test_register_dependency()
        self.main_package.install(True)
        self.assertTrue(self.dependency.installed)
        self.assertFalse(self.dependency.explicitly_installed)
        self.assertTrue(self.dependency2.installed)
        self.assertFalse(self.dependency2.explicitly_installed)
        self.assertTrue(self.main_package.installed)
        self.assertTrue(self.main_package.explicitly_installed)

    def test_installation_failed(self):
        self.test_register_dependency()
        self.main_package.install_process = raise_exception
        self.assertRaises(package.PackageInstallationError, self.main_package.install)

    def test_installation_failed_on_dependency(self):
        self.test_register_dependency()
        self.dependency.install_process = raise_exception
        self.assertRaises(package.DependencyInstallationError, self.main_package.install)

