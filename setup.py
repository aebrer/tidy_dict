from setuptools import setup
from setuptools import find_packages

setup(name='NestedDict',
      description='A Nested Dictionary Class',
      long_description='A dictionary that can be used to easily make nested dictionaries and export to CSV as tidy data',
      version='1.0.0',
      url='https://github.com/atomoton/nested_dict',
      license='gpl-3.0',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      zip_safe=False
      )
