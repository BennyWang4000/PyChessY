from setuptools import find_packages, setup


def readme():
    with open("README.md", "r") as readme:
        long_description = readme.read()
    return long_description


setup(
    name="PyChessY",
    version="1.2.0",
    author="BennyWang4000",
    author_email="wang.benny0102@gmail.com",
    description="ChessY with Python",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=["PyChessY", "PyChessY.*"]),
    keywords="chess",
    url="https://github.com/BennyWang4000/PyChessY",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
