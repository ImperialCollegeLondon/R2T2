from setuptools import setup

r2t2_classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Topic :: Utilities",
]

tests_require = ["pytest", "pytest-flake8", "pytest-mypy"]


setup(
    name="R2T2",
    version=0.1,
    author="Research Computing Service, Imperial College London",
    author_email="rcs-support@imperial.ac.uk",
    url="https://github.com/ImperialCollegeLondon/R2T2",
    tests_require=tests_require,
    py_modules=["r2t2"],
    description="Research references tracking tool",
    license="MIT",
    classifiers=r2t2_classifiers,
    python_requires=">=3.0",
)
