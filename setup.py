from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in texcity_builders/__init__.py
from texcity_builders import __version__ as version

setup(
	name="texcity_builders",
	version=version,
	description="Lead Management",
	author="Thirvusoft Private Limited",
	author_email="info@thirvusoft.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
