from setuptools import setup, find_packages

setup(name='zirc',
      version='1.0.2',
      description="Python IRCP Library",
      url='https://github.com/itslukej/zirc',
      author='Luke J.',
      author_email='me+zirc@lukej.me',
      license='GNL',
      packages=["zirc"],
      install_requires=['six'],
      include_package_data=True,
      zip_safe=False)
