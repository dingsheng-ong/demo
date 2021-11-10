from setuptools import find_packages, setup
from demo import config

setup(
    name='demo',
    version=config.VERSION,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)