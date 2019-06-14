import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="query-cannon",
    version="0.0.1",
    author="Andrew Redmond",
    author_email="andrewpredmond@gmail.com",
    description="python DNS Tester",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git-codecommit.us-west-2.amazonaws.com/v1/repos/query-cannon",
    packages=setuptools.find_packages(),
    install_requires=[
        'Click',
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={  # Optional
        'console_scripts': [
            'qcan=src.entry_point:entry_point',
        ],
    },
)