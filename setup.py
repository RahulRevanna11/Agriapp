from setuptools import setup, find_packages

setup(
    name='fertilizer_calculator.py',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-fuzzy',
    ],
)
