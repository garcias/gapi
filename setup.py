from setuptools import setup, find_packages

setup(
    name = 'gapi',
    version = 0.1,
    description = 'Convenience functions to use Google API services',
    url = 'https://github.com/garcias/gapi',
    author = 'Simon Garcia',
    author_email = 'garcias@kenyon.edu',
    license='MIT',
    keywords='google api',
    packages=find_packages(),
    install_requires=[ 'requests', 'httplib2', 'oauth2client', 'apiclient', ],
    python_requires='>=3.6',
    include_package_data=True,
)
