from setuptools import setup, find_packages
def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='banditvis',
    version='0.7',
    description='A library for simulating and visualizing bandit algorithms.',
    long_description=readme(),
    url='https://github.com/alexrutar/banditvis',
    author='Alex Rutar',
    author_email='arutar@uwaterloo.ca',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='bandit machine learning',
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests', 'checklist.py']),
    install_requires=[
        'numpy>=1.10',
        'pyyaml>=3.11',
        'scipy>=0.18',
        'matplotlib>=2'
    ],
    package_data={'': ['LICENSE', 'README.md', 'banditvis/user_defaults.pkl']},
    include_package_data=True,
    entry_points={'console_scripts': ['banditvis = banditvis.__main__:main']},
    zip_safe=False
)
