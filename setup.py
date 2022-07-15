from setuptools import setup

setup(
    name="grubbs-test",
    version="0.1",
    description="Grubbs test implementation following GraphPad's calculator",
    author="Thomaz Guadagnini Ramalheira",
    author_email="thzgr@tuta.io",
    url="https://github.com/thzgr/Grubbs-Test",
    package_dir={"grubbs":"grubbs_test"},
    packages=["grubbs"],
    python_requires = ">3",
    install_requires = [
        "numpy",
        "scipy"
    ]
)