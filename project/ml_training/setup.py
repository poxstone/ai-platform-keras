from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['tensorflow==2.9.3']

setup(
    name='fashion_mnist',
    version='0.1',
    author = 'poxstone',
    author_email = 'pox@gmail.com',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='Simple keras GCP test',
    requires=['tensorflow']
)
