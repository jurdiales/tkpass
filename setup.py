from setuptools import setup, find_packages

setup(
    name='tkpass',
    version='0.2.0',
    author='Jesus',
    author_email='jesus.urdiales93@gmail.com',
    description='Password generator using tkinter',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    package_data={"tkpass": ["password.ico", "*.tcl", "theme/*", "theme/light/*", "theme/dark/*", "forest-light/*", "forest-dark/*"]},
    install_requires=["tk", "pyperclip"],
)
