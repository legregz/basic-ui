from setuptools import setup, find_packages

setup(
    name='basic_ui',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # Inclure explicitement les fichiers data dans mon_package
        'basic_ui': ['config/*.json'],
    },
    install_require=[
        'pygame>=2.6.0'
    ],
    author='Legregz',
    description="basic ui is a package for pygame to create interfaces easly based on json files",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read()
)