from setuptools import setup, find_packages

setup(
    name='wrcli',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='none',
    description='CLI for Alnoda workspaces',
    long_description=open('README.md').read(),
    install_requires=[],
    url='https://github.com/bluxmit/workspace-cli',
    author='bluxmit',
    author_email='bluxmit@gmail.com'
)