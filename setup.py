import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="entrio2mail",
    version="1.0.0",
    author="schef",
    author_email="",
    description="Send entrio status to mail",
    long_description=long_description,
    url="https://github.com/schef/entrio2mail",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
    #    'console_scripts': [
    #        'pyzer-service-runner = pyzer_cli.common.service_runner:run',
    #    ],
    },
    install_requires=[
    ],
)
