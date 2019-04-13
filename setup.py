import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='cloudflare-dynamic-ip',
    version='0.0.1',
    author='Cristian Steib',
    author_email='cristiansteib@gmail.com',
    description='Service to auto update ip in cloudflare',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    package_data={'resources': ['*', '**/*', '**/**/*']},
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'License :: Other/Proprietary License',
    ],
)
