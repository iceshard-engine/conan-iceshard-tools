class Premake(object):
    premake_installer = "premake_installer/5.0.0-alpha14@bincrafters/stable"
    premake_generators_vstudio = {
        "11": "vs2012",
        "12": "vs2013",
        "14": "vs2015",
        "15": "vs2017",
        "16": "vs2019",
    }

    def __init__(self, package):
        self._package = package

    def generate(self, config_file = None):
        package = self._package
        settings = self._package.settings

        # Get the proper premake5 action
        premake_action = "gmake"
        if settings.compiler == "Visual Studio":
            premake_action = self.premake_generators_vstudio.get(str(settings.compiler.version), "vs2019")

        premake_commandline = "premake5 {} --arch={}".format(premake_action, settings.arch)
        if config_file != None:
            premake_commandline += " --file={}".format(config_file)

        # Generate premake5 projects
        package.run(premake_commandline)
