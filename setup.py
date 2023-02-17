from setuptools import setup, find_packages

setup(
    name='vcs_p_pack',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'parse_work=package.vcs_p:parse_work'
        ]
    },
)
