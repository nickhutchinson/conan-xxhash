import textwrap
from conans import ConanFile, CMake, tools


class XxhashConan(ConanFile):
    name = "xxhash"
    description = (
        "xxHash is an extremely fast non-cryptographic hash "
        "algorithm, working at speeds close to RAM limits"
    )
    version = "0.6.5"
    license = "BSD"
    url = "https://cyan4973.github.io/xxHash/"
    repo_url = "https://github.com/Cyan4973/xxHash"

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    generators = "cmake"
    no_copy_sources = True

    def source(self):
        tools.get("%s/archive/v%s.zip" % (self.repo_url, self.version))
        tools.replace_in_file(
            "xxHash-%s/cmake_unofficial/CMakeLists.txt" % self.version,
            "cmake_minimum_required (VERSION 2.8.12)",
            textwrap.dedent(
                """\
                cmake_minimum_required (VERSION 2.8.12)
                cmake_policy(SET CMP0063 NEW)  # Symbol visibility
                include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
                conan_basic_setup()
                """
            ).rstrip(),
        )
        tools.replace_in_file(
            "xxHash-%s/cmake_unofficial/CMakeLists.txt" % self.version,
            "install(TARGETS xxhash",
            textwrap.dedent(
                """\
                install(TARGETS xxhash
                    RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
                """
            ).rstrip(),
        )

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.verbose = True
        if not self.options.shared:
            cmake.definitions["CMAKE_C_VISIBILITY_PRESET"] = "hidden"

        if self.settings.compiler == "Visual Studio" and self.options.shared:
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = True

        cmake.configure(source_folder="xxHash-%s/cmake_unofficial" % self.version)
        return cmake

    def build(self):
        self.configure_cmake().build()

    def package(self):
        self.configure_cmake().install()

    def package_info(self):
        self.cpp_info.libs = ["xxhash"]

    def configure(self):
        del self.settings.compiler.libcxx
