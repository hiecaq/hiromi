from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hiromi',
    use_scm_version=True,
    description='A command line anime tracker.',
    long_description=long_description,
    url='https://github.com/quinoa42/hiromi',
    author='quinoa42',
    author_email='',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='Bangumi, MyAnimeList',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'beautifulsoup4==4.6.0', 'lxml==4.1.1', 'requests==2.18.4'
    ],
    python_requires='>=3.6, <4',
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    entry_points={
        'console_scripts': ['hiromi=hiromi.cli:main']
    }
)
