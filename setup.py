import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="musicXML-synthesizer", # Replace with your own username
    version="0.9.8",
    author="ykhorizon",
    author_email="ykhorizon@gmail.com",
    description="A package to transform solola output to standard musicXML format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SoloLa-Platform/MusicXML-Synthesizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
