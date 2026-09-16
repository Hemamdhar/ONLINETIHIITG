from setuptools import setup, find_packages

setup(
    name="underwater_surveillance",
    version="1.0.0",
    description="AI-Based Underwater Visual Surveillance Pipeline",
    author="Hemamdhar Dakarapu",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "opencv-python>=4.8.0",
        "pillow>=10.0.0",
        "ultralytics>=8.0.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0"
    ],
    entry_points={
        "console_scripts": [
            "underwater-surveillance=underwater_surveillance.cli:main",
        ],
    },
    python_requires=">=3.8",
)
