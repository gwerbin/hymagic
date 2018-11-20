from setuptools import setup, find_packages

setup(
    name = 'hymagic',
    packages = find_packages(),
    version = '0.1.1',
    description = 'IPython magic for hylang',
    author = 'Todd Iverson',
    author_email = 'tiverson@smumn.edu',
    maintainer = 'Greg Werbin',
    maintainer_email = 'outthere@me.gregwerbin.com',
    url = 'https://github.com/gwerbin/hymagic',   # use the URL to the github repo
    download_url = 'https://github.com/gwerbin/hymagic/archive/0.1.1.tar.gz', # I'll explain this in a second
    keywords = ['hylang', 'IPython extension', 'IPython magic'], # arbitrary keywords
    classifiers = ["Development Status :: 3 - Alpha"]
)
