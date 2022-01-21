import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brep_part_finder",
    version="develop",
    author="The Fusion Energy Development Team",
    author_email="mail@jshimwell.com",
    description="A Python package to identify the part ID number in Brep",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fusion-energy/brep_part_finder",
    packages=setuptools.find_packages(),
    package_data={
        "brep_part_finder": [
            "requirements.txt",
            "README.md",
            "LICENSE",
            "tests/*.stl",
        ]
    },
    classifiers=[
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy"
        # 'cadquery' currently only available via conda
    ],
)
