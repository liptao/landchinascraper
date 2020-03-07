from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    readme = readme_file.read()

requirements = ['requests>=2.22.0', 'beautifulsoup4>=4.8.2',
                'pandas>=1.0.1', 'openpyxl>=3.0.3', 'selenium>=3.141.0']

setup(
    name='landchinascraper',
    version='0.0.2',
    author='Lipei Tao',
    author_email='eric@lipeitao.com',
    description='Scrapes landchina.com transactions.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/liptao/landchinascraper/',
    packages=find_packages('src'),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
)
