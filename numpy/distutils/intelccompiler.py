from __future__ import division, absolute_import, print_function

import sys

from distutils.unixccompiler import UnixCCompiler
from numpy.distutils.exec_command import find_executable
from numpy.distutils.ccompiler import simple_version_match


class IntelCCompiler(UnixCCompiler):
    """A modified Intel compiler compatible with a GCC-built Python."""
    compiler_type = 'intel'
    cc_exe = 'icc'
    cc_args = 'fPIC'

    def __init__(self, verbose=0, dry_run=0, force=0):
        UnixCCompiler.__init__(self, verbose, dry_run, force)
        self.cc_exe = 'icc -fPIC'
        compiler = self.cc_exe
        self.set_executables(compiler=compiler,
                             compiler_so=compiler,
                             compiler_cxx=compiler,
                             archiver='xiar' + ' cru',
                             linker_exe=compiler,
                             linker_so=compiler + ' -shared')


class IntelItaniumCCompiler(IntelCCompiler):
    compiler_type = 'intele'

    # On Itanium, the Intel Compiler used to be called ecc, let's search for
    # it (now it's also icc, so ecc is last in the search).
    for cc_exe in map(find_executable, ['icc', 'ecc']):
        if cc_exe:
            break


class IntelEM64TCCompiler(UnixCCompiler):
    """
    A modified Intel x86_64 compiler compatible with a 64bit GCC-built Python.
    """
    compiler_type = 'intelem'
    cc_exe = 'icc -m64 -fPIC'
    cc_args = "-fPIC"

    def __init__(self, verbose=0, dry_run=0, force=0):
        UnixCCompiler.__init__(self, verbose, dry_run, force)
        self.cc_exe = 'icc -m64 -fPIC'
        compiler = self.cc_exe
        self.set_executables(compiler=compiler,
                             compiler_so=compiler,
                             compiler_cxx=compiler,
                             archiver='xiar' + ' cru',
                             linker_exe=compiler,
                             linker_so=compiler + ' -shared')


if sys.platform == 'win32':
    from distutils.msvc9compiler import MSVCCompiler

    class IntelCCompilerW(MSVCCompiler):
        """
        A modified Intel compiler compatible with an MSVC-built Python.
        """
        compiler_type = 'intelw'

        def __init__(self, verbose=0, dry_run=0, force=0):
            MSVCCompiler.__init__(self, verbose, dry_run, force)
            version_match = simple_version_match(start='Intel\(R\).*?32,')
            self.__version = version_match

        def initialize(self, plat_name=None):
            MSVCCompiler.initialize(self, plat_name)
            self.cc = self.find_exe("icl.exe")
            self.lib = self.find_exe("xilib")
            self.linker = self.find_exe("xilink")
            self.compile_options = ['/nologo', '/O3', '/MD', '/W3',
                                    '/Qstd=c99']
            self.compile_options_debug = ['/nologo', '/Od', '/MDd', '/W3',
                                          '/Qstd=c99', '/Z7', '/D_DEBUG']

    class IntelEM64TCCompilerW(IntelCCompilerW):
        """
        A modified Intel x86_64 compiler compatible with
        a 64bit MSVC-built Python.
        """
        compiler_type = 'intelemw'

        def __init__(self, verbose=0, dry_run=0, force=0):
            MSVCCompiler.__init__(self, verbose, dry_run, force)
            version_match = simple_version_match(start='Intel\(R\).*?64,')
            self.__version = version_match

