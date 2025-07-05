"""
Setup script for Vietnamese Password Converter
"""

from setuptools import setup, find_packages

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vietnamese-password-converter",
    version="1.0.0",
    author="Vietnamese Password Converter Team",
    author_email="contact@example.com",
    description="Convert Vietnamese text to passwords and vice versa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/vietnamese-password-converter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=[
        # No external dependencies required
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vietnamese-password-converter=src.cli.main:main",
            "vn-pwd-convert=src.cli.main:main",
        ],
    },
    keywords="password vietnamese text conversion t9 keypad security",
    project_urls={
        "Bug Reports": "https://github.com/example/vietnamese-password-converter/issues",
        "Source": "https://github.com/example/vietnamese-password-converter",
        "Documentation": "https://github.com/example/vietnamese-password-converter/wiki",
    },
)