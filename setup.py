import setuptools

with open("ReadMe.md", "r") as rd_f:
    long_description = rd_f.read()

setuptools.setup(
    name="SVGVideoMaker",
    version="0.4.1",
    author="Yann Zavattero",
    author_email="yann.zavattero@hotmail.com",
    description="Creator of video from svg with cairosvg, ffmpeg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evayann/SVGVideoMaker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)