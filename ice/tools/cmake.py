class GenCMake(object):
    cmake_installer = "cmake_installer/3.16.0@conan/stable"

    def __init__(self, package):
        self._package = package

    def generate(self, compiler):
        pass
        # if compiler == "Visual Studio":
        #     generator = premake_generators_vstudio.get(str(self.settings.compiler.version), "vs2019")
        #     return generator
        # else:
        #     return "<unknown_compiler>"
