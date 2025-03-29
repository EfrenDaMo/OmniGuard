from setuptools import setup, find_packages

setup(
    name="omni",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "flask",
        "python-dotenv",
        "mysql-connector-python",
        "cryptography",
        "flask-cors",
        "flask-limiter",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-flask",
            "pytest-cov",
        ]
    },
    entry_points={
        "console_scripts": [
            "omni=omni.app:main",
        ]
    },
)
