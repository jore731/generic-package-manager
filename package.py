class PackageInstallationError(Exception):
    pass


class DependencyInstallationError(PackageInstallationError):
    pass


class Package(object):
    def __init__(self, name: str):
        self.name: str = name
        self.installed: bool = False
        self.explicitly_installed: bool = False
        self.dependencies: list = []
        self.required_by: list = []

    def install(self, explicitly_installed: bool = False):
        """
        Verifies dependencies and installs the package

        :param explicitly_installed: If true, the package would be marked as explicitly installed, preventing automatic
        uninstallations.

        :return: None

        :raise PackageInstallationError:  Either installation process failed or dependency installation process failed
        """
        if self.dependencies is not []:
            self.install_dependencies()
        try:
            self.install_process()
        except Exception:
            raise PackageInstallationError from Exception

        self.installed = True
        self.explicitly_installed = explicitly_installed

    def install_dependencies(self):
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
        pass
