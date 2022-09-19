import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
REQUIREMENTS = (HERE / "requirements.txt").read_text()

setup(
    name="interfacy-core",
    version="0.0.1",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Žiga IvanŠek",
    author_email="ziga.ivansek@gmail.com",
    url="https://github.com/zigai/",
    python_requires=">=3.10",
    license="",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    install_requires=REQUIREMENTS,
)
