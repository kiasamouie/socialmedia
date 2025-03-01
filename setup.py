from setuptools import setup, find_packages

def readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()

def read_requirements():
    """Reads requirements.txt and returns a list of dependencies."""
    with open("requirements.txt", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

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
    packages=find_packages(exclude=["tests", "docs"]),
    install_requires=read_requirements(),
    include_package_data=True,
)
