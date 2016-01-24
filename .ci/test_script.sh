#!/bin/bash

set -e

python --version
python -c "import numpy; print('numpy %s' % numpy.__version__)"

QT_API=pyqt4 nosetests