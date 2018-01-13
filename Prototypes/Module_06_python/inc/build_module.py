from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True
import numpy

setup(
    cmdclass={
        'build_ext': build_ext
    },
    ext_modules=[
        Extension("module_06_cy",
                  ["module_06_cy.pyx"],
                  include_dirs=[numpy.get_include()]
                  ),
    ]
)
