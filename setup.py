import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="netverify", # Replace with your pypi username
    version="1.0.0",
    author="Du'An Lightfoot",
    author_email="duanl@labeveryday.com",
    description="Network verification tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/labeveryday",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=required
)
