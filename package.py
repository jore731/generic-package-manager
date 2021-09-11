class PackageInstallationError(Exception):
    pass


class DependenceLoopError(Exception):
    pass


class DependencyInstallationError(PackageInstallationError):
    pass


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

        if self.installed and explicitly_installed:
            print(f"        {self.name} is already installed")
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
        print(f"        {self.name} successfully installed")

