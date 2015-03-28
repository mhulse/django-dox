from setuptools import setup, find_packages

VERSION = '1.0.0'

setup (
    name = 'dox',
    version = VERSION,
    description = 'Yet another Django flat pages app on steroids.',
    author = 'Micky Hulse',
    author_email = 'micky@registerguard.com',
    maintainer = 'Micky Hulse',
    maintainer_email = 'micky@registerguard.com',
    url = 'https://github.com/registerguard/django-dox',
    license = 'http://www.apache.org/licenses/LICENSE-2.0',
    platforms = ['any'],
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
)