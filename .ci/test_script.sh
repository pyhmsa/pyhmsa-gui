#!/bin/bash

set -e -o pipefail -u


python --version
python -c "import numpy; print('numpy %s' % numpy.__version__)"
python -c "import scipy; print('scipy %s' % scipy.__version__)"


QT_API=pyqt4 nosetests