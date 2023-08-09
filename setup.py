import setuptools

setuptools.setup(
    name="sspaf",
    version="0.0.10",
    description="A superglued single page application framework",
    author="plusleft",
    url="https://github.com/0xleft/sspaf",
    packages=setuptools.find_packages(),
    install_requires=[
        'flask',
        'waitress',
    ],
    entry_points={
        'console_scripts': [
            'sspaf = sspaf.sspaf_bin:main'
        ]
    }
)