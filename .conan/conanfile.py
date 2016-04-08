from conans import ConanFile, CMake
import os

############### CONFIGURE THESE VALUES ##################
default_user = "local"
default_channel = "testing"
#########################################################

channel = os.getenv("CONAN_CHANNEL", default_channel)
username = os.getenv("CONAN_USERNAME", default_user)

class CPRConanPackageTest(ConanFile):
    generators = "cmake"
    requires = "cpr/1.2.0@%s/%s" % (username, channel)
    settings = "os", "compiler", "arch", "build_type"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")
        
    def test(self):
        self.run(".%sbin%scpr_demo" % (os.sep, os.sep))
        