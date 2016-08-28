from setuptools import setup, find_packages
def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='banditvis',
    version='0.4',
    description='A library for simulating and visualizing bandit algorithms.',
    long_description=readme(),
    url='https://github.com/alexrutar/banditvis',
    author='Alex Rutar',
    author_email='arutar@uwaterloo.ca',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='bandit machine learning',
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests', 'checklist.py']),
    install_requres=[
        'numpy',
        'pyyaml',
        'scipy',
        'matplotlib'
    ],
    package_data={'': ['LICENSE', 'README.md', 'user_defaults.pkl']},
    include_package_data=True,
    entry_points={'console_scripts': ['banditvis = banditvis.__main__:main']},
    zip_safe=False
)