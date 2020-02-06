from setuptools import setup, find_packages

r2t2_classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Topic :: Utilities",
]

tests_require = ["pytest", "pytest-flake8", "pytest-mypy"]
precommit = ["pre-commit"]

setup(
    name="R2T2",
    version="0.3.1",
    author="Research Computing Service, Imperial College London",
    author_email="rcs-support@imperial.ac.uk",
    url="https://github.com/ImperialCollegeLondon/R2T2",
    install_requires=["wrapt"],
    tests_require=tests_require,
    extras_require={"dev": tests_require + precommit},
    packages=find_packages("."),
    description="Research references tracking tool",
    license="MIT",
    classifiers=r2t2_classifiers,
    python_requires=">=3.0",
)
