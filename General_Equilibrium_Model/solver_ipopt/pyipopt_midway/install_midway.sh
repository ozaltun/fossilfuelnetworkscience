
# setup environment
export IPOPT_DIR="`pwd`/Ipopt-3.12.5/build"


#Install IPOPT
echo "installing IPOPT now"

cd Ipopt-3.12.5

mkdir -p build

cd build

../configure

make -j12

make test

make install

IPOPT_DIR=`pwd`

echo $IPOPT_DIR

export LD_LIBRARY_PATH=IPOPT_DIR/lib:$LD_LIBRARY_PATH

echo $LD_LIBRARY_PATH

cd ../../
echo " IPOPT is installed"

#install PYIPOPT
tar xfv pyipopt.tar

cd pyipopt

python3.6 setup.py build

python3.6 setup.py install --user

cd examples

python3.6 hs071.py

echo " PYIPOPT is tested and installed"
