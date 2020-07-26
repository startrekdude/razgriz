import setuptools

from shutil import rmtree

with open("README.md") as f:
	long_description = f.read()

with open("requirements.txt") as f:
	requirements = f.readlines()

setuptools.setup(
	name="razgriz",
	version="1.0",
	author="Sam Haskins",
	description="Encrypted paper vaults for 2FA recovery codes",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/startrekdude/razgriz",
	license="GPLv3",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: OS Independent",
	],
	install_requires=requirements,
	python_requires=">=3.8",
)

rmtree("build")
rmtree("razgriz.egg-info")