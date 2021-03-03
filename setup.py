from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='p3exporter',
    version='0.1.0',
    description='Python Programmable Prometheus exporter',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://codeaffen.org/projects/p3exporter',
    author='Christian Meißner',
    author_email='cme@codeaffen.org',
    license='GPLv3',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='monitoring prometheus exporter example',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    package_data={'p3exporter': ['static/*', 'templates/*']},
    install_requires=[
        'prometheus-client',
        'PyYAML',
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'p3exporter=p3exporter:main',
        ],
    },
)
