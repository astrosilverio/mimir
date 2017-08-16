import os
from setuptools import setup


version_file_py = os.path.join(os.path.split(__file__)[0], "hogwarts/version.py")
with open(version_file_py) as version_file:
    __version__ = ""
    exec(compile(version_file.read(), version_file_py, 'exec'))


if __name__ == '__main__':
    setup(name='hogwarts',
          version=__version__,
          description='Framework for writing/running text adventure games',
          url='http://github.com/astrosilverio/hogwarts',
          author='astrosilverio',
          author_email='astrosilverio@gmail.com',
          license='MIT',
          packages=['hogwarts'],
          install_requires=['braga'],
          test_suite='nose.collector',
          tests_require=['nose'])
