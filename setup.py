from setuptools import setup, find_packages
setup(
    name='mhscr_interpreter',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mhscr=mhscr_interpreter.main:Run'
        ]
    }
)