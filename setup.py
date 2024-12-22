from setuptools import setup, find_packages

setup(
    name="childcare_project",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "openpyxl",
        "customtkinter",
    ],
    entry_points={
        "console_scripts": [
            "childcare_app=main:main",
        ],
    },
)
