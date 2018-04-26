# -*- coding: utf-8 -*-
"""
Usage: pip install .[dev]
"""

import re
from setuptools import setup, find_packages

# Get the version number
with open('./aiida_tbmodels/__init__.py') as f:
    match_expr = "__version__[^'\"]+(['\"])([^'\"]+)"
    version = re.search(match_expr, f.read()).group(2).strip()

if __name__ == '__main__':
    setup(
        name='aiida-tbmodels',
        version=version,
        description='AiiDA Plugin for running TBmodels',
        author='Dominik Gresch',
        author_email='greschd@gmx.ch',
        url='http://z2pack.ethz.ch/aiida-plugins/aiida-tbmodels',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha', 'Environment :: Plugins',
            'Framework :: AiiDA', 'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Physics'
        ],
        keywords='tbmodels aiida workflows',
        packages=find_packages(exclude=['aiida']),
        include_package_data=True,
        setup_requires=['reentry'],
        reentry_register=True,
        install_requires=['future', 'aiida-core', 'aiida-bands-inspect'],
        extras_require={
            'dev': ['pytest', 'aiida-pytest', 'yapf==0.21', 'pre-commit']
        },
        entry_points={
            'aiida.calculations': [
                'tbmodels.eigenvals = aiida_tbmodels.calculations.eigenvals:EigenvalsCalculation',
                'tbmodels.parse = aiida_tbmodels.calculations.parse:ParseCalculation',
                'tbmodels.slice = aiida_tbmodels.calculations.slice:SliceCalculation',
                'tbmodels.symmetrize = aiida_tbmodels.calculations.symmetrize:SymmetrizeCalculation',
            ],
            'aiida.parsers': [
                'tbmodels.model = aiida_tbmodels.parsers.model:ModelParser',
            ],
        },
    )
