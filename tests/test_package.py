import logging
import unittest

from package import Package, PackageInstallationError, DependencyInstallationError, PackageRemovalError, \
    DependenceLoopError

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s [%(levelname)s]: %(message)s")


def raise_exception():
    raise Exception


class PackageInstallingTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_package(self):
        new_package = Package("nano")
        self.assertEqual(new_package.name, "nano")

    def test_install_package(self):
        new_package = Package("nano")
        new_package.install(explicitly_installed=True)
        self.assertTrue(new_package.installed)
        self.assertTrue(new_package.explicitly_installed)

    def test_package_not_installed(self):
        new_package = Package("nano")
        self.assertFalse(new_package.installed)

    def test_register_dependency(self):
        self.main_package = Package("main_package")
        self.dependency1 = Package("dependency1")
        self.dependency2 = Package("dependency2")
        self.main_package.depends_on(self.dependency1)
        self.main_package.depends_on(self.dependency2)
        self.assertEqual(self.main_package.dependencies[0].name, "dependency1")

    def test_install_package_with_dependencies(self):
        self.test_register_dependency()
        self.main_package.install(explicitly_installed=True)
        self.assertTrue(self.dependency1.installed)
        self.assertFalse(self.dependency1.explicitly_installed)
        self.assertTrue(self.dependency2.installed)
        self.assertFalse(self.dependency2.explicitly_installed)
        self.assertTrue(self.main_package.installed)
        self.assertTrue(self.main_package.explicitly_installed)

    def test_installation_failed(self):
        self.test_register_dependency()
        self.main_package.install_process = raise_exception
        self.assertRaises(PackageInstallationError, self.main_package.install)

    def test_installation_failed_on_dependency(self):
        self.test_register_dependency()
        self.dependency1.install_process = raise_exception
        self.assertRaises(DependencyInstallationError, self.main_package.install)

