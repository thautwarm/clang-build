"""
clang-build:
  TODO: module docstring...
"""



import os
from subprocess import call, check_output
import sys
import getopt



from enum import Enum
class TargetType(Enum):
    SharedLibrary = 0
    StaticLibrary = 1
    Executable    = 2
class BuildType(Enum):
    Default        = 0
    Release        = 1
    MinSizeRel     = 2
    RelWithDebInfo = 3
    Debug          = 4



from sys import platform as _platform
executable_suffix     = ''
shared_library_prefix = ''
shared_library_suffix = ''
static_library_prefix = ''
static_library_suffix = ''
if _platform == "linux" or _platform == "linux2":
    # Linux
    shared_library_prefix = 'lib'
    shared_library_suffix = '.so'
    static_library_prefix = 'lib'
    static_library_suffix = '.a'
elif _platform == "darwin":
    # OS X
    shared_library_prefix = 'lib'
    shared_library_suffix = '.dylib'
    static_library_prefix = 'lib'
    static_library_suffix = '.a'
elif _platform == "win32":
    # Windows
    executable_suffix     = '.exe'
    shared_library_prefix = ''
    shared_library_suffix = '.dll'
    static_library_prefix = ''
    static_library_suffix = '.dll'



class Target:
    targetDirectory    = ""
    name               = "main"
    targetType         = TargetType.Executable

    includeDirectories = []
    compileFlags       = []
    linkFlags          = []

    buildType          = BuildType.Default
    buildDirectory     = "build"

    sourceFiles        = []
    headerFiles        = []

    def __init__(self):
        pass

    def build(self):
        if self.targetType == TargetType.Executable:
            self.prefix = ""
            self.suffix = executable_suffix
        elif self.targetType == TargetType.SharedLibrary:
            self.prefix = shared_library_prefix
            self.suffix = shared_library_suffix
        elif self.targetType == TargetType.StaticLibrary:
            self.prefix = static_library_prefix
            self.suffix = static_library_suffix

        command = "clang"
        for file in self.sourceFiles:
            command += " " + file

        for flag in self.compileFlags:
            command += " " + flag

        outname = self.prefix + self.name + self.suffix
        command += " -o " + self.buildDirectory + "/" + outname

        os.makedirs(self.buildDirectory, exist_ok=True)
        call(command, shell=True)




def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--verbose",
                        help="activate verbose build",
                        action="store_true")
    parser.add_argument("-d", "--directory",
                        help="set the root source directory")
    args = parser.parse_args()

    if args.verbose:
        print("Verbosity turned on. This functionality is not yet implemented")

    callingdir = os.getcwd()
    workingdir = os.getcwd()
    if args.directory:
        workingdir = args.directory
        print("working: " + workingdir)


    # Check for build configuration toml file
    if os.path.isfile("clang-build.toml"):
        pass
    # Otherwise we try to build it as a simple hello world or mwe project
    else:
        # Create target
        target = Target()
        target.targetDirectory = workingdir

        from glob import glob

        # Search for header files
        headers = []
        for ext in ('*.hpp', '*.hxx'):
            headers += glob(os.path.join(workingdir, ext))

        # Search for source files
        sources = []
        for ext in ('*.cpp', '*.cxx'):
            sources += glob(os.path.join(workingdir, ext))

        # Set target
        target.headerFiles = headers
        target.sourceFiles = sources

        # List of targets
        targets = [target]

    # Build the targets
    for target in targets:
        target.build()



if __name__ == "__main__":
    sys.exit(main())