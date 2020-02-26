# Originally contributed by Lorne McIntosh.
# Modified by Eric Xu
# Further modification by random internet people.

# You will probably have to edit this file in unpredictable ways
# if you want pyipopt to work for you, sorry.

# When I installed Ipopt from source, I used the
# --prefix=/usr/local
# option, so this is where I want pyipopt to look for my ipopt installation.
# I only installed from source because the ipopt packaging
# for my linux distribution was buggy,
# so by the time you read this the bugs have probably been fixed
# and you will want to specify a different directory here.
#IPOPT_DIR = '/usr/local/'
IPOPT_DIR = '/home/ozaltun/research/fossilfuelnetworkscience/General_Equilibrium_Model/solver_ipopt/pyipopt_midway/Ipopt-3.12.5/build/'
#IPOPT_DIR = '/pool001/ozaltun/ipopt_test/'
import os
from distutils.core import setup
from distutils.extension import Extension

# NumPy is much easier to install than pyipopt,
# and is a pyipopt dependency, so require it here.
# We need it to tell us where the numpy header files are.
import numpy
numpy_include = numpy.get_include()

# I personally do not need support for lib64 but I'm keeping it in the code.
def get_ipopt_lib():
    for lib_suffix in ('lib', 'lib64'):
        d = os.path.join(IPOPT_DIR, lib_suffix)
        if os.path.isdir(d):
            return d

IPOPT_LIB = get_ipopt_lib()
if IPOPT_LIB is None:
    raise Exception('failed to find ipopt lib')

IPOPT_INC = os.path.join(IPOPT_DIR, 'include/coin/')

FILES = ['src/callback.c', 'src/pyipoptcoremodule.c']
print('hello!')
print(IPOPT_INC, IPOPT_LIB)
print('bye!')
# The extra_link_args is commented out here;
# that line was causing my pyipopt install to not work.
# Also I am using coinmumps instead of coinhsl.
pyipopt_extension = Extension(
        'pyipoptcore',
        FILES,
        #extra_link_args=['-Wl,--rpath','-Wl,'+ IPOPT_LIB],
        #extra_link_args = ['-L/pool001/ozaltun/ipopt_test/bin/'],
	#extra_link_args = ['-L/pool001/ozaltun/ipopt_test/lib -Wl,-rpath=/pool001/ozaltun/ipopt_test/lib -Wl,--no-as-needed -Wl,--sysroot=/'],
	library_dirs=[IPOPT_LIB],
        libraries=[
            'ipopt', 'coinblas',
            'coinhsl',  ###changed this one
            #'coinmumps',
            'coinmetis',
            'coinlapack','dl','m',
            ],
        include_dirs=[numpy_include, IPOPT_INC],
        )

setup(
        name="pyipopt",
        version="0.8",
        description="An IPOPT connector for Python",
        author="Eric Xu",
        author_email="xu.mathena@gmail.com",
        url="https://github.com/xuy/pyipopt",
        packages=['pyipopt'],
        package_dir={'pyipopt' : 'pyipoptpackage'},
        ext_package='pyipopt',
        ext_modules=[pyipopt_extension],
        )

