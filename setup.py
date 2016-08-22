from setuptools import setup

setup(name='banditvis',
      version='0.1',
      description='A library for simulating bandit algorithms.',
      url='https://github.com/alexrutar/banditvis',
      author='Alex Rutar',
      author_email='arutar@uwaterloo.ca',
      license='MIT',
      packages=['banditvis'],
      install_requres=['numpy', 'pyyaml', 'scipy', 'matplotlib'],
      zip_safe=False)