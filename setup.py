from setuptools import setup, find_packages

setup(
    name="corelated_logs",
    version="0.0.6",
    packages=find_packages(exclude=["tests"]),
    install_requires=["structlog==18.2.0", "wrapt==1.10.11", "pre-commit-hooks==1.4.0"],
    url="",
    license="BSD",
    author="sohit kumar",
    author_email="sumitk002@gmail.com",
    test_suite="tests",
    description="A python library to generate corelation id and bind it to headers in outgoing request",
)
