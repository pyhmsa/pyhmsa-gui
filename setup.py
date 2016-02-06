#!/usr/bin/env python

# Standard library modules.
import os
import sys
import glob
from distutils.core import Command
from subprocess import check_call

# Third party modules.
from setuptools import setup, find_packages

# Local modules.
import versioneer

# Globals and constants variables.
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class _bdist_fpm(Command):

    description = 'Build using fpm (Effing Package Management)'

    user_options = [('dist-dir=', 'd',
                     "directory to put final built distributions in "
                     "[default: dist]"), ]

    def initialize_options(self):
        self.dist_dir = None

    def finalize_options(self):
        if self.dist_dir is None:
            self.dist_dir = "dist"

    def _run(self, target):
        setup_filepath = os.path.join(BASEDIR, 'setup.py')

        python_bin = 'python3' if sys.version_info.major == 3 else 'python'
        version = '%i.%i' % (sys.version_info.major, sys.version_info.minor)

        args = ['fpm',
                '-s', 'python',
                '-t', target,
                '--force',
                '--verbose',
                '--maintainer', 'Philippe Pinard <philippe.pinard@gmail.com>',
                '--category', 'science',
                '--depends', "%s >= %s" % (python_bin, version),
                '--depends', python_bin + '-numpy',
                '--depends', python_bin + '-six',
                '--depends', python_bin + '-matplotlib',
                '--depends', python_bin + '-pyside',
                '--depends', python_bin + '-hmsa',
                '--no-python-dependencies',
                '--python-bin', python_bin,
                '--name', python_bin + '-hmsa-gui',
                setup_filepath]
        check_call(args)

        self.mkpath(self.dist_dir)
        for srcfilepath in glob.glob('*.%s' % target):
            self.move_file(srcfilepath, self.dist_dir)

class bdist_deb(_bdist_fpm):

    description = 'Build deb '

    def run(self):
        self._run('deb')

# Get the long description from the relevant file
with open('README.rst', 'r') as f:
    long_description = f.read()

cmdclass = versioneer.get_cmdclass()
cmdclass['bdist_deb'] = bdist_deb

setup(name='pyHMSA-gui',
      version=versioneer.get_version(),
      description='Graphical components to represent HMSA specification',
      long_description=long_description,

      author='Philippe Pinard',
      author_email='philippe.pinard@gmail.com',
      maintainer='Philippe Pinard',
      maintainer_email='philippe.pinard@gmail.com',

      url='http://pyhmsa.readthedocs.org',
      license='MIT',
      keywords='microscopy microanalysis hmsa file format gui',

      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Physics',
        ],

      packages=find_packages(),
      package_data={'pyhmsa_gui.util': ['icons/*.rcc']},

      tests_require=['nose', 'coverage'],
      install_requires=['pyHMSA', 'qtpy', 'matplotlib', 'numpy', 'six', 'setuptools'],

      test_suite='nose.collector',

      zip_safe=True,

      entry_points=\
        {'pyhmsa_gui.spec.condition.calibration':
            ['CalibrationConstant = pyhmsa_gui.spec.condition.calibration:CalibrationConstantWidget',
             'CalibrationLinear = pyhmsa_gui.spec.condition.calibration:CalibrationLinearWidget',
             'CalibrationPolynomial = pyhmsa_gui.spec.condition.calibration:CalibrationPolynomialWidget',
             'CalibrationExplicit = pyhmsa_gui.spec.condition.calibration:CalibrationExplicitWidget'],
         'pyhmsa_gui.spec.condition':
            ['AcquisitionPoint = pyhmsa_gui.spec.condition.acquisition:AcquisitionPointWidget',
             'AcquisitionMultipoint = pyhmsa_gui.spec.condition.acquisition:AcquisitionMultipointWidget',
             'AcquisitionRasterLinescan = pyhmsa_gui.spec.condition.acquisition:AcquisitionRasterLinescanWidget',
             'AcquisitionRasterXY = pyhmsa_gui.spec.condition.acquisition:AcquisitionRasterXYWidget',
             'AcquisitionRasterXYZ = pyhmsa_gui.spec.condition.acquisition:AcquisitionRasterXYZWidget',

             'DetectorCamera = pyhmsa_gui.spec.condition.detector:DetectorCameraWidget',
             'DetectorSpectrometer = pyhmsa_gui.spec.condition.detector:DetectorSpectrometerWidget',
             'DetectorSpectrometerCL = pyhmsa_gui.spec.condition.detector:DetectorSpectrometerCLWidget',
             'DetectorSpectrometerWDS = pyhmsa_gui.spec.condition.detector:DetectorSpectrometerWDSWidget',
             'DetectorSpectrometerXEDS = pyhmsa_gui.spec.condition.detector:DetectorSpectrometerXEDSWidget',

             'ElementalID = pyhmsa_gui.spec.condition.elementalid:ElementalIDWidget',
             'ElementalIDXray = pyhmsa_gui.spec.condition.elementalid:ElementalIDXrayWidget',

             'Instrument = pyhmsa_gui.spec.condition.instrument:InstrumentWidget',

             'ProbeEM = pyhmsa_gui.spec.condition.probe:ProbeEMWidget',
             'ProbeTEM = pyhmsa_gui.spec.condition.probe:ProbeTEMWidget',

             'RegionOfInterest = pyhmsa_gui.spec.condition.region:RegionOfInterestWidget',

             'SpecimenPosition = pyhmsa_gui.spec.condition.specimenposition:SpecimenPositionWidget',

             'CompositionElemental = pyhmsa_gui.spec.condition.composition:CompositionElementalWidget',

             'Specimen = pyhmsa_gui.spec.condition.specimen:SpecimenWidget',
    #            'SpecimenMultilayer = pyhmsa_gui.spec.condition.specimen:SpecimenMultilayerWidget'
            ],
         'pyhmsa_gui.spec.datum':
            ['Analysis0D.Table = pyhmsa_gui.spec.datum.analysis:Analysis0DTableWidget',
             'Analysis1D.Table = pyhmsa_gui.spec.datum.analysis:Analysis1DTableWidget',
             'Analysis1D.Graph = pyhmsa_gui.spec.datum.analysis:Analysis1DGraphWidget',
             'Analysis2D.Table = pyhmsa_gui.spec.datum.analysis:Analysis2DTableWidget',
             'Analysis2D.Graph = pyhmsa_gui.spec.datum.analysis:Analysis2DGraphWidget',

             'AnalysisList0D.Table = pyhmsa_gui.spec.datum.analysislist:AnalysisList0DTableWidget',
             'AnalysisList0D.Graph = pyhmsa_gui.spec.datum.analysislist:AnalysisList0DGraphWidget',
             'AnalysisList1D.Table = pyhmsa_gui.spec.datum.analysislist:AnalysisList1DTableWidget',
             'AnalysisList1D.Graph = pyhmsa_gui.spec.datum.analysislist:AnalysisList1DGraphWidget',
             'AnalysisList2D.Table = pyhmsa_gui.spec.datum.analysislist:AnalysisList2DTableWidget',
             'AnalysisList2D.Graph = pyhmsa_gui.spec.datum.analysislist:AnalysisList2DGraphWidget',

             'ImageRaster2D.Table = pyhmsa_gui.spec.datum.imageraster:ImageRaster2DTableWidget',
             'ImageRaster2D.Graph = pyhmsa_gui.spec.datum.imageraster:ImageRaster2DGraphWidget',
             'ImageRaster2DSpectral.Table = pyhmsa_gui.spec.datum.imageraster:ImageRaster2DSpectralTableWidget',
             'ImageRaster2DSpectral.Graph = pyhmsa_gui.spec.datum.imageraster:ImageRaster2DSpectralGraphWidget',
             ],
         },

      cmdclass=cmdclass,
     )
