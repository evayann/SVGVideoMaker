import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SVGVideoMaker", # Replace with your own username
    version="0.0.1",
    author="Yann Zavattero",
    author_email="yann.zavattero@hotmail.com",
    description="Creator of video from svg with cairosvg, ffmpeg",
    long_description="TODO",
    long_description_content_type="text/markdown",
    url="https://github.com/LINK",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)