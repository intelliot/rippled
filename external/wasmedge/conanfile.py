from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import get, copy, rmdir
from conan.tools.build import check_min_cppstd
import os

required_conan_version = ">=1.53.0"

class WasmEdgeConan(ConanFile):
    name = "wasmedge"
    description = "WasmEdge is a lightweight, high-performance, and extensible WebAssembly runtime"
    license = "Apache-2.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/WasmEdge/WasmEdge"
    topics = ("webassembly", "wasm", "runtime", "compiler")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_tools": [True, False],
        "build_aot": [True, False],
        "build_plugins": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "build_tools": False,
        "build_aot": False,
        "build_plugins": False,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, 17)
        # Explicitly set compiler version to avoid the error
        if not self.settings.compiler.version:
            self.output.warning("Compiler version not defined, setting a default value")
            if self.settings.compiler == "gcc":
                self.settings.compiler.version = "11"
            elif self.settings.compiler == "clang":
                self.settings.compiler.version = "13"
            elif self.settings.compiler == "apple-clang":
                self.settings.compiler.version = "13"
            elif self.settings.compiler == "Visual Studio":
                self.settings.compiler.version = "16"
            else:
                self.output.warning(f"Unknown compiler: {self.settings.compiler}, please set version manually")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["WASMEDGE_BUILD_TESTS"] = False
        tc.variables["WASMEDGE_BUILD_AOT_RUNTIME"] = self.options.build_aot
        tc.variables["WASMEDGE_BUILD_TOOLS"] = self.options.build_tools
        tc.variables["WASMEDGE_PLUGIN_WASI_NN_BACKEND"] = "none"
        tc.variables["WASMEDGE_PLUGIN_WASI_CRYPTO"] = False
        tc.variables["WASMEDGE_PLUGIN_PROCESS"] = False
        tc.variables["WASMEDGE_PLUGIN_WASM_BPF"] = False
        tc.variables["WASMEDGE_BUILD_PLUGINS"] = self.options.build_plugins
        tc.variables["WASMEDGE_LINK_LLVM_STATIC"] = not self.options.shared
        tc.variables["WASMEDGE_LINK_TOOLS_STATIC"] = not self.options.shared
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "WasmEdge")
        self.cpp_info.set_property("cmake_target_name", "WasmEdge::wasmedge")
        
        # Libraries
        self.cpp_info.components["wasmedgelib"].libs = ["wasmedge"]
        self.cpp_info.components["wasmedgelib"].requires = []
        
        if self.options.build_aot:
            self.cpp_info.components["wasmedgeaot"].libs = ["wasmedge-aot"]
            self.cpp_info.components["wasmedgeaot"].requires = ["wasmedgelib"]
        
        # System libs
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["wasmedgelib"].system_libs.extend(["pthread", "dl", "m"]) 