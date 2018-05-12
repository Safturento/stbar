Stbar is a task replacement designed for linux tiling window managers. It allows easy configuration and addition of custom modules with a helper class to simplify the process of writing new modules. 

## Installation 
### From source
First clone the repo and cd
```
git clone https://github.com/Safturento/stbar.git
cd stbar
```
from here you can either run ```./install``` or you can manually run the components below
```
sudo apt-get install build-essential libgl1-mesa-dev
pip install --user --index-url=http://download.qt.io/snapshots/ci/pyside/5.9/latest/ pyside2 --trusted-host download.qt.io

python3 setup.py sdist
python3 setup.py install --user
```
