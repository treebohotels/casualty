from setuptools import find_packages, setup

setup(
    name="casualty",
    version="0.1.0",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "structlog==18.2.0",
        "wrapt==1.10.11",
        "pre-commit-hooks==1.4.0",
        "black",
    ],
    url="",
    license="MIT",
    author="Sohit Kumar",
    author_email="sumitk002@gmail.com",
    test_suite="tests",
    description="A python library to generate co-relation id and bind it to headers in outgoing request",
)
