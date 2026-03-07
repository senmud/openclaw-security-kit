from setuptools import setup, find_packages

setup(
    name="openclaw-security-kit",
    version="0.1.0",
    packages=find_packages(),
    description="OpenClaw Security Hardening Kit - 一站式 Agent 安全加固套件",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Volcano Security Team",
    url="https://github.com/senmud/openclaw-security-kit",
    install_requires=[
        "sentence-transformers>=2.2.2",
        "numpy>=1.21.0",
        "pydantic>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
)