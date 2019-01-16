apt-get update
apt-get dist-upgrade
apt-get install python make xterm python-pip
sudo pip install --upgrade pip
sudo -H pip install --upgrade pip
sudo -H pip install pipenv
sudo pip install --upgrade setuptools
sudo pip install twisted

sudo python setup.py build
sudo python setup.py install

sudo mkdir -p /usr/local/lib/python2.7/dist-packages/minicps/pymodbus/
sudo cp minicps/pymodbus/* /usr/local/lib/python2.7/dist-packages/minicps/pymodbus/

sudo mkdir -p /usr/local/lib/python2.7/dist-packages/minicps-1.1.3-py2.7.egg/minicps/pymodbus
sudo cp minicps/pymodbus/* /usr/local/lib/python2.7/dist-packages/minicps-1.1.3-py2.7.egg/minicps/pymodbus/

cd ..

git clone git://github.com/mininet/mininet.git
cd mininet/util
./install.sh -a