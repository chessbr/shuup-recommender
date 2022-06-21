# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="shuup-recommender",
    version="0.1.0",
    description="Shuup Recommender",
    license="Apache-2.0",
    author="Christian Hess",
    author_email="christianhess.rlz@gmail.com",
    url="https://github.com/chessbr/shuup-recommender",
    packages=find_packages(),
    install_requires=[
        "pandas==0.22.0",
        "numpy==1.22.0",
        "django-pandas==0.5.0",
    ],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 2.7",
    ]
)
