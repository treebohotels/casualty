from setuptools import find_packages, setup


setup(
    name="casualty",
    version="0.1.8",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "structlog==18.2.0",
        "wrapt==1.10.11",
        "pre-commit-hooks==1.4.0",
        "mock==2.0.0",
        "pytest==3.8.2",
        "pytest-mock==1.10.0",
        "pytest-cov"
    ],
    url="",
    python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    license="MIT",
    author="Sohit Kumar",
    author_email="sumitk002@gmail.com",
    test_suite="tests",
    description="A python library to generate co-relation id and bind it to headers in outgoing request",
)
