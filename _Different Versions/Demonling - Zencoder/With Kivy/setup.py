#!/usr/bin/env python3
"""
Setup script for Demonling game
"""

from setuptools import setup, find_packages

# Read requirements
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

# Read README if it exists
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Demonling: Rise of the Realm Lord - A mobile RPG game built with Kivy"

setup(
    name="demonling",
    version="1.0.0",
    description="A mobile RPG game where you rise to become the ultimate Demon Lord",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Demonling Team",
    author_email="contact@demonling.com",
    url="https://github.com/demonling/demonling",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.7',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment :: Role-Playing",
    ],
    keywords="game rpg mobile kivy android ios",
    entry_points={
        'console_scripts': [
            'demonling=main:main',
        ],
    },
    package_data={
        'demonling': ['assets/*', 'assets/*/*'],
    },
)