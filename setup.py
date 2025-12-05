from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pizzaa",
    version="1.0.0",
    description="A FastAPI-based Pizza Store Management System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "fastapi==0.123.4",
        "uvicorn[standard]==0.38.0",
        "sqlitedict==2.1.0",
        "pydantic==2.12.5",
    ],
)