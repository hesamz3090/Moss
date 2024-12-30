from setuptools import setup, find_packages

AUTHOR_NAME = "Hesam Aghajani"
AUTHOR_CONTACT = "hesamz3090@gmail.com"

setup(
    name='moss-crawler',
    version='0.1.0',
    author=AUTHOR_NAME,
    author_email=AUTHOR_CONTACT,
    description='A simple web crawler that classifies URLs and performs multi-threaded requests.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/moss-crawler',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.25.1',
        'beautifulsoup4>=4.9.3',
    ],
    entry_points={
        'console_scripts': [
            'moss=moss:main',
        ],
    },
)
