from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='moss',
    version='2.0.0',
    author='Hesam Aghajani',
    author_email='hesamz3090@gmail.com',
    description='A simple web crawler that classifies URLs and performs',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hesamz3090/moss',
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
            'moss=moss.main:main',
        ],
    },
)
