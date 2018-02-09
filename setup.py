from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='get-secret',
    version='0.0.1',
    py_modules=['get_secret'],
    test_suite='tests',
    description='Simple tool to fetch secrets for your application.',
    long_description=readme(),
    author='Sandeep Jadoonanan',
    author_email='jsanweb@gmail.com',
    url='https://github.com/tunedmystic/get-secret',
    download_url=(
        'https://github.com/tunedmystic/get-secret/archive/0.0.1.tar.gz'
    ),
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=['secret', 'env', 'docker'],
)
