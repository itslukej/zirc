from setuptools import setup, find_packages
from sys import version_info, exit, stderr

with open("PyPi-README.rst") as f:
    long_description = f.read().replace("\r", "")

if version_info < (2, 7, 0) or (version_info[0] == 3 and version_info < (3, 2, 0)):
    stderr.write('zIRC requires Python 2.7 or 3.2 and higher')
    exit(-1)

setup(name='zirc',
      version='1.2.9+git',
      description='Python IRCP Library',
      long_description=long_description,
      url='https://github.com/itslukej/zirc',
      author='Luke J.',
      author_email='me+zirc@lukej.me',
      license='GNU',
      packages=find_packages(),
      install_requires=['six'],
      extras_require={
          'pysocks': ['pysocks'],
          'pysocks:sys_platform=="win32" and python_version == "2.7"': ['win_inet_pton']
      },
      python_requires='>=2.7,!=3.0.*,!=3.1.*',
      include_package_data=True,
      zip_safe=False,
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Natural Language :: English',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Communications :: Chat :: Internet Relay Chat',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ])
