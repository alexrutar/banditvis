from setuptools import setup, find_packages

setup(name='banditvis',
    version='0.2',
    description='A library for simulating and visualizing bandit algorithms.',
    url='https://github.com/alexrutar/banditvis',
    author='Alex Rutar',
    author_email='arutar@uwaterloo.ca',
    classifiers=[
        'Programming Language :: Python :: 3.5'
    ],
    keywords='bandit machine learning',
    license='MIT',
    packages=find_packages(),
    install_requres=['numpy', 'pyyaml', 'scipy', 'matplotlib'],
    entry_points={'console_scripts': ['banditvis = banditvis.__main__:main']},
    zip_safe=False)