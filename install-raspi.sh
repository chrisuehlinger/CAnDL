#!/bin/bash -ixe
# Source: https://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/

# Install dependencies
sudo apt-get purge -y wolfram-engine
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y \
                      build-essential cmake pkg-config \
                      libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev \
                      libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
                      libxvidcore-dev libx264-dev libgtk2.0-dev libatlas-base-dev gfortran \
                      python2.7-dev python3-dev python-tk \
                      libffi-dev libssl-dev

# Download the OpenCV source code
cd ~
wget -O opencv.zip https://github.com/opencv/opencv/archive/3.2.0.zip
unzip opencv.zip
rm opencv.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.2.0.zip
unzip opencv_contrib.zip
rm opencv_contrib.zip

# Install pip
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo -H pip install --upgrade pip

# Install virtualenv
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/.cache/pip

echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile
source ~/.profile

mkvirtualenv candl -p python2
source ~/.profile
workon candl

# Install Python dependencies
pip install numpy
pip install twisted
pip install autobahn
pip install service_identity
pip install matplotlib

# Compile and Install OpenCV
cd ~/opencv-3.2.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.2.0/modules \
    -D BUILD_EXAMPLES=ON ..

make
sudo make install
sudo ldconfig

cd ~/.virtualenvs/candl/lib/python2.7/site-packages/
ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so
