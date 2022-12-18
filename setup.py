from setuptools import setup
import os

VERSION = "0.1.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-gunicorn",
    description="Run a Datasette server using Gunicorn",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-gunicorn",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-gunicorn/issues",
        "CI": "https://github.com/simonw/datasette-gunicorn/actions",
        "Changelog": "https://github.com/simonw/datasette-gunicorn/releases",
    },
    license="Apache License, Version 2.0",
    classifiers=[
        "Framework :: Datasette",
        "License :: OSI Approved :: Apache Software License",
    ],
    version=VERSION,
    packages=["datasette_gunicorn"],
    entry_points={"datasette": ["gunicorn = datasette_gunicorn"]},
    install_requires=["datasette>0.63.2", "gunicorn"],
    extras_require={"test": ["pytest", "pytest-asyncio", "cogapp"]},
    python_requires=">=3.7",
)
