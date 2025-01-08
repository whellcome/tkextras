from setuptools import setup, find_packages

setup(
    name="tkextras",
    version="1.0.0",
    description="A Tkinter utility module for enhanced widgets rendering",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dietmar Steinle",
    license="MIT",
    url="https://github.com/whellcome/tkextras",
    packages=find_packages(),
    keywords=["tkinter", "ttk", "gui"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Tcl/Tk Extensions",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=[
        "pandas>=1.0",
        "tk",
    ],
    python_requires=">=3.8",
)
