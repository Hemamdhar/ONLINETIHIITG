from setuptools import setup, find_packages

setup(
    name="underwater_surveillance",
    version="1.0.0",
    author="Hemamdhar Dakarapu",
    description="Real-Time AI-Based Underwater Visual Surveillance Software Package",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.22.0",
        "opencv-python>=4.7.0",
        "pillow>=9.0.0",
        "torch>=1.13.0",
        "ultralytics>=8.0.0",
        "pandas>=1.5.0",
        "matplotlib>=3.5.0",
    ],
    entry_points={
        "console_scripts": [
            "underwater-surveillance=underwater_surveillance.cli:main",
        ],
    },
)
