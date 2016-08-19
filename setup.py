import os
from setuptools import setup

long_desc = """
OPAL Referral is a plugin for the OPAL web framework that provides functionality for making
referrals between hospital teams or to hospital departments/clinics.

Source code and documentation available at https://github.com/openhealthcare/opal-referral/
"""

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='opal-referral',
    version='0.2.0',
    packages=['referral'],
    include_package_data=True,
    license='GPL3',
    description='OPAL Referral Portal plugin ',
    long_description=long_desc,
    url='http://opal.openhealthcare.org.uk/',
    author='Open Health Care UK',
    author_email='hello@openhealthcare.org.uk',
)
