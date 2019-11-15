from setuptools import setup

setup(
    name='BrewRunner',
    version='1.0',
    packages=['BrewRunner'],
    entry_points={
        'console_scripts': [
            'BrewRunner = BrewRunner.__main__:main'
            ]
        },
    )
