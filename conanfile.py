# from enum import Enum
from conans import ConanFile, MSBuild, CMake
from conans import tools

from ice.tools.premake import GenPremake5
from ice.tools.cmake import GenCMake
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

        source_info = self.conan_data["sources"][self.ice_source_entry(self.version)]
        if "branch" in source_info:
            git = tools.Git(folder=self._ice.source_dir)
            git.clone(source_info["url"], source_info["branch"])
            if "commit" in source_info:
                git.checkout(source_info["commit"])
        elif "tag" in source_info:
            git = tools.Git(folder=self._ice.source_dir)
            git.clone(source_info["url"], source_info["tag"])
        else:
            tools.get(**source_info)

    def build(self):
        self._ice.source_dir = "{}-{}".format(self.name, self.version)
        self._ice.out_dir = self._ice.source_dir
        with tools.chdir(self._ice.source_dir):
            self.ice_build()

    # Iceshard method implementations
    def ice_init(self, generator):
        self._ice = IceProperties()

        if generator == "none"
            pass

        elif generator == "premake5":
            self._ice.generator = GenPremake5(self)
            self._ice.build_requires.append(self._ice.generator.premake_installer)

        elif generator == "cmake":
            self._ice.generator = GenCMake(self)
            self._ice.build_requires.append(self._ice.generator.cmake_installer)

        else:
            self.output.error("Unknown project generator")

    def ice_configure(self):
        if self.settings.compiler == "Visual Studio":
            del self.settings.compiler.runtime

    def ice_source_entry(self, version):
        return version

    def ice_generate(self):
        self._ice.generator.generate()

    def ice_build(self):
        pass

    def ice_build_msbuild(self, solution, build_types=["Debug", "Release"]):
        msbuild = MSBuild(self)
        for build_type in build_types:
            msbuild.build(solution, build_type=build_type)

    def ice_build_cmake(self, build_types=["Debug", "Release"], definitions={}):
        for build_type in build_types:
            cmake = CMake(self, build_type=build_type)
            for name, value in definitions.items():
                cmake.definitions[name] = value
            cmake.configure(source_dir="..", build_dir="build")
            cmake.build()

    def ice_build_make(self, build_types=["Debug", "Release"]):
        self.output.error("The 'IceTools.ice_build_make' method is not yet implemented!")

##
## Conan package class.
class ConanIceshardTools(ConanFile):
    name = "conan-iceshard-tools"
    version = "0.5.4"

    exports = "ice/*"
