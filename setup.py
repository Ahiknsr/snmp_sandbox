from setuptools import setup, find_packages

requirements = open('requirements.txt').read().strip().split('\n')

setup(
    name = "pdumaster",
    version = "0.1",
    packages = find_packages(),
    install_requires = requirements,
)