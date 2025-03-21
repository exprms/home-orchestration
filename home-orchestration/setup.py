from setuptools import find_packages, setup

setup(
    name="home_orchestration",
    packages=find_packages(exclude=["home_orchestration_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
