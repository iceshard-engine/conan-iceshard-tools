class GenCMake(object):
    cmake_installer = "cmake_installer/3.16.0@conan/stable"

    def __init__(self, package):
        self._package = package

    def generate(self, compiler):
        pass
