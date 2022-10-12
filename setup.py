import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="checkscore", # Replace with your own username
    version="0.2.0",
    author="Newton Poudel",
    author_email="hinewton25@gmail.com",
    description="A package to auto fill methods in jupyter notebook for SCORE interaction.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenDevICON/Checkscore",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)