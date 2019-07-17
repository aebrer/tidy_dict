import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nested_dict",
    version="1.0.0",
    author="Andrew E Brereton",
    author_email="andrew@brereton.me",
    description="A tool for easy Nested Dictionaries with option to output tidy CSV files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atomoton/nested_dict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
)