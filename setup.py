from setuptools import setup, find_packages

setup(
    name='basic_ui',
    version='0.4.1',
    packages=find_packages(),
    install_require=[
        'pygame>=2.6.0'
    ],
)