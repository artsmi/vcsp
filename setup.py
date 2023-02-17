from setuptools import setup, find_packages

setup(
    name='vcs_p_pack',
    version='0.0.8',
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'parse_work=package.__main__:main'
        ]
    },
    package_dir={"": "package"},
    packages=find_packages("package"),
    install_requires=['']
)
