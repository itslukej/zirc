from setuptools import setup, find_packages
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = "This library implements the IRC protocol, it's an event-driven IRC Protocol framework."


setup(name='zirc',
      version='1.2.4',
      description='Python IRCP Library',
      long_description=long_description,
      url='https://github.com/itslukej/zirc',
      author='Luke J.',
      author_email='me+zirc@lukej.me',
      license='GNU',
      packages=find_packages(),
      install_requires=['six', 'pysocks'],
      include_package_data=True,
      zip_safe=False,
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Topic :: Communications :: Chat :: Internet Relay Chat',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ])
