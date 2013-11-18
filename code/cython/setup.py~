#http://docs.cython.org/src/userguide/tutorial.html
#run with:
#> python setup.py build_ext --inplace

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [ Extension("distance", ["distance.pyx"])#,
		#Extension("c1", ["c1.pyx"]),
		#Extension("c2", ["c2.pyx"]),
		#Extension("c3", ["c3.pyx"]),
		#Extension("csum", ["csum.pyx"])
		]

setup(
  name = 'Cython Test Scripts',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
