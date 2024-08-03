#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="yagni",
    version="0.0.3",
    description="You are probably gonna need it: a collection of useful Python utilities aggregated over many years of development.",
    packages=find_packages(),
    install_requires=[
        # 'six',
    ],
    extras_require={
        'dev': [
            'black',
            'isort',
            'pytest',
            'pytest-cov',
            'radon',
            'xenon',
        ],
    },
    python_requires=">=3.8",
)
