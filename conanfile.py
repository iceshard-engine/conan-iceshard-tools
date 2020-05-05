# from enum import Enum
from conans import ConanFile, MSBuild
from conans import tools

from tools.premake import Premake
from tools.cmake import Cmake
import os

##
## Helper class to easily extend it with arbitrary properties during runtime
class IceProperties(object):
    def __init__(self):
        self.build_requires = []

##
## Base class for Conan package recipes following the 'IceShard' package requiremenets.
class IceTools(object):
    # Default conan method implementations
    def configure(self):
        self.ice_configure()

    def source(self):
        self._ice.source_dir = "{}-{}".format(self.name, self.version)

        source_info = self.conan_data["sources"][self.version]
        if "branch" in source_info:
            git = tools.Git(folder=self._ice.source_dir)
            git.clone(source_info["url"])
            git.checkout(source_info["branch"])
        else:
            tools.get(**source_info)

    def build(self):
        with tools.chdir(self._ice.source_dir):
            self.ice_build()

    # Iceshard method implementations
    def ice_init(self, generator):
        self._ice = IceProperties()

        if generator == "premake5":
            self._ice.generator = Premake(self)
            self._ice.build_requires.append(self._ice.generator.premake_installer)

        elif generator == "cmake":
            self._ice.generator = Cmake(self)
            self._ice.build_requires.append(self._ice.generator.cmake_installer)

        else:
            self.output.error("Unknown project generator")

    def ice_configure(self):
        if self.settings.compiler == "Visual Studio":
            del self.settings.compiler.runtime

    def ice_build(self):
        pass

    def ice_build_msbuild(self, solution, build_types=["Debug", "Release"]):
        msbuild = MSBuild(self)
        for build_type in build_types:
            msbuild.build(solution, build_type=build_type)

    def ice_build_cmake(self, build_types=["Debug", "Release"]):
        cmake = CMake(self)

        # Multi configuration CMake project
        if cmake.is_multi_configuration:
            os.mkdir("build")

            with tools.chdir("build"):
                cmmd = 'cmake ".." {}'.format(cmake.command_line)
                self.run(cmmd)

                for build_type in build_types:
                    self.run("cmake --build . --config {}".format(build_type))

        # Single configuration CMake project
        else:
            for build_type in build_types:

                build_path = "build_{}".format(build_type)
                os.mkdir(build_path)

                with tools.chdir(build_path):
                    self.output.info("Building {}".format(build_type))
                    self.run("cmake .. {} -DCMAKE_BUILD_TYPE={}".format(cmake.command_line, build_type))
                    self.run("cmake --build .")
                    shutil.rmtree("CMakeFiles")
                    os.remove("CMakeCache.txt")

##
## Conan package class.
class ConanIceshardTools(ConanFile):
    name = "conan-iceshard-tools"
    version = "0.2"

    exports = "tools/*"
