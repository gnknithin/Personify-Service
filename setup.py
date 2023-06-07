from setuptools import find_packages, setup

setup(
    name="Personify-Service",
    version="0.1.0",
    description="A Personify Server for any Service Utility",
    url="https://github.com/gnknithin/Personify-Service",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    test_suit="tests"
)
