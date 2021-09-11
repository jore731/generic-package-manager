class PackageInstallationError(Exception):
    pass


class DependenceLoopError(Exception):
    pass


class DependencyInstallationError(PackageInstallationError):
    pass


class PackageRemovalError(Exception):
    pass


class CleanupProcessError(Exception):
    pass


class DependentPackageFoundError(Exception):
    def __init__(self, package):
        super().__init__(f"         {package.name} is still needed")


class Package(object):
    def __init__(self, name: str):
        self.name: str = name
        self.installed: bool = False
        self.explicitly_installed: bool = False
        self.dependencies: list = []
        self.dependent_packages: list = []

    def depends_on(self, package):
        """
        Registers `package` as a dependency (and self as a dependent package of `package`)

        :param package: Package to be registered as dependency

        :return: None

        :raise DependenceLoopError: When trying to register a dependent package as a dependency
        """
        if package in self.dependent_packages:
            raise DependenceLoopError()

        if package not in self.dependencies:
            self.dependencies.append(package)
        if self not in package.dependent_packages:
            package.required_by(self)

    def required_by(self, package):
        """
        Registers `package` as a dependent package (and self as a dependency of `package`)

        :param package: Package to be registered as dependent package

        :return: None

        :raise DependenceLoopError: When trying to register a dependency as a dependent package
        """
        if package in self.dependencies:
            raise DependenceLoopError()

        if package not in self.dependent_packages:
            self.dependent_packages.append(package)
        if self not in package.dependencies:
            package.depends_on(self)

    def install(self, explicitly_installed: bool = False):
        """
        Verifies dependencies and installs the package

        :param explicitly_installed: If true, the package would be marked as explicitly installed, preventing automatic
        removal.

        :return: None

        :raise PackageInstallationError:  Either installation process failed or dependency installation process failed
        """
        if self.dependencies is not []:
            self._install_dependencies()

        if self.installed:
            if explicitly_installed:
                self.explicitly_installed = True
                print(f"         {self.name} is already installed")
            return None
        try:
            self.install_process()
        except Exception:
            raise PackageInstallationError() from Exception

        self.installed = True
        self.explicitly_installed = explicitly_installed

    def _install_dependencies(self):
        """
        If dependencies are detected, proceeds to install them

        :return: None

        :raise PackageInstallationError: If any of the dependent packages fails to install
        """
        for dependence in self.dependencies:
            try:
                dependence.install()
            except PackageInstallationError:
                raise DependencyInstallationError(
                    f"There was a problem installing some dependencies: {dependence.name}")

    def install_process(self):
        """Depending on the package, the install process might vary. For now, the package installation can be assumed as
        nothing else than success"""
        print(f"         {self.name} successfully installed")

    def remove(self, explicity_removal: bool = True):
        """

        Verifies dependent packages and removes the package if it is safe to do it

        :param explicity_removal: If False, notifies when no longer needed before removing

        :raise PackageRemovalError:  Package removal process failed
        :raise CleanupProcessError:  Dependent package removal process failed
        :raise DependentPackageFoundError:  Package is still needed by another package
        """
        if self.dependent_packages is not []:
            try:
                self._verify_dependent_packages()
            except DependentPackageFoundError as exc:
                print(exc)
                return None

        if not explicity_removal:
            print(f"         {self.name} is no longer needed")

        if explicity_removal and not self.installed:
            print(f"         {self.name} is not installed")
            return None
        try:
            self.remove_process()
        except Exception:
            raise PackageRemovalError() from Exception

        self.installed = False
        self.explicitly_installed = False

        if self.dependencies is not []:
            self._clean_dependencies()

    def _verify_dependent_packages(self):
        """
        :raise DependentPackageFoundError: When a dependent package is still installed
        """
        for package in self.dependent_packages:
            if package.installed:
                raise DependentPackageFoundError(self)

    def _clean_dependencies(self):
        """
        Clean dependent packages after removing a package

        :raise CleanupProcessError: If a problem happens on removing some dependency
        """
        for dependence in self.dependencies:
            try:
                if not dependence.explicitly_installed:
                    dependence.remove(explicity_removal=False)
            except DependentPackageFoundError as exc:
                pass
            except PackageRemovalError:
                raise CleanupProcessError(f"There was a problem removing some dependencies: {dependence.name}")

    def remove_process(self):
        """Depending on the package, the removal process might vary. For now, the package removal can be assumed as
        nothing else than success (assuming the dependent package verification is already done"""
        print(f"         {self.name} successfully removed")
