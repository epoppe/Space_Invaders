"""
Setup-skript for Space Invaders.
Installerer spillet som en Python-pakke.
"""

from setuptools import setup, find_packages

setup(
    name="space_invaders",
    version="1.0.0",
    description="En moderne versjon av det klassiske Space Invaders-spillet",
    author="Erik Poppe",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pygame>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "space-invaders=src.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Environment :: MacOS X",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment :: Arcade",
    ],
    python_requires=">=3.8",
) 