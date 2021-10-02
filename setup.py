from setuptools import setup

setup(
    name="git-syncer",
    version="0.0.5",
    description="Allows cron job control and command execution on a remote machine using git infrastructure",
    author="Asaf Kali",
    author_email="unknown@gmail.com",
    url="https://github.com/asaf-kali/git-syncer",
    install_requires=["pycron>=3.0.0"],
    license="https://github.com/asaf-kali/git-syncer/blob/main/LICENSE",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
