
from setuptools import setup, find_packages
from yas.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='yas',
    version=VERSION,
    description='Yas - yAn aliasing manager for your terminal commands!',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Ahmed Amr',
    author_email='ahmedamron@gmail.com',
    url='https://github.com/AhmedAmr/yas',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'yas': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        yas = yas.main:main
    """,
)
