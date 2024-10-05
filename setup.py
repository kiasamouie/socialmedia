from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name="socialmedia",
    version="0.0.1",
    description="socialmedia",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/kiasamouie/socialmedia",
    author="Kia Samouie",
    author_email="thekiadoe@gmail.com",
    keywords="socialmedia",
    license="MIT",
    packages=["instagram"],
    install_requires=[],
    include_package_data=True,
)
