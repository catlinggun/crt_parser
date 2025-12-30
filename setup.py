import setuptools

setuptools.setup(
    name='crt_parse',
    version='0.1.3',
    packages=setuptools.find_packages(),
    url='',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    author='Dave Catling',
    author_email='dave.catling@avalanchesec.com',
    description='Grabs domain data from crt.sh, attempts to resolve, and parses data into CSV format.',
    install_requires='requests==2.26.0',
    python_requires='>=3.7.3',
    entry_points={'console_scripts': ['crt_parse = crt_parse.crt_parse:main']}
)