from setuptools import setup, find_packages
from main import NAME, AUTHOR, CONTACT, DESCRIPTIONS, VERSION, URL
import os


def read_requirements():
    with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
        return f.read().splitlines()


setup(
    name=NAME.lower(),
    version=VERSION,
    author=AUTHOR,
    author_email=CONTACT,
    description=DESCRIPTIONS,
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url=URL,
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'moss=main:main',
        ],
    },
)
