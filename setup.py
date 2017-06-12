# -*- coding: utf-8 -*-
"""
setup: usage: pip install -e .[graphs]
"""

from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='aiida-tbmodels',
        version='0.0.0a1',
        description='AiiDA Plugin for running TBmodels',
        author='Dominik Gresch',
        author_email='greschd@gmx.ch',
        license='GPL',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Plugins',
            'Framework :: AiiDA',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Physics'
        ],
        keywords='tbmodels aiida workflows',
        packages=find_packages(exclude=['aiida']),
        include_package_data=True,
        setup_requires=[
            'reentry'
        ],
        reentry_register=True,
        install_requires=[
            'future',
            'aiida-core',
            'aiida-bandstructure-utils'
        ],
        extras_require={
        },
        entry_points={
            'aiida.calculations': [
                'tbmodels.eigenvals = aiida_tbmodels.calculations.eigenvals:EigenvalsCalculation',
                'tbmodels.parse = aiida_tbmodels.calculations.parse:ParseCalculation',
                'tbmodels.slice = aiida_tbmodels.calculations.slice:SliceCalculation',
                'tbmodels.symmetrize = aiida_tbmodels.calculations.symmetrize:SymmetrizeCalculation',
            ],
            'aiida.data': [
                'tbmodels.list = aiida_tbmodels.data.list:ListData',
            ],
            'aiida.parsers': [
                'tbmodels.model = aiida_tbmodels.parsers.model:ModelParser',
            ],
            'aiida.workflows': [
                'tbmodels.bandevaluation = aiida_tbmodels.workflows.bandevaluation:BandevaluationWorkflow',
            ],
        },
    )
