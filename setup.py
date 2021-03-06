from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='cloudflare_dynamic_ip',
    version='0.0.3',
    author='Cristian Steib',
    author_email='cristiansteib@gmail.com',
    description='Service to auto update ip in cloudflare',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    package_data={'resources': ['*', '**/*', '**/**/*']},
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'cloudflare-dynamic-ip = cloudflare_dynamic_ip.service:main']
    },
    packages=find_packages(),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'License :: Other/Proprietary License',
    ],
)
