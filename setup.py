try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
        'name': 'foreperiodanalysis',
        'description': 'Foreperiod Analysis',
        'author': 'Mika Tammi',
        'url': 'https://github.com/mikatammi/foreperiodanalysis',
        'download_url': 'https://github.com/mikatammi/foreperiodanalysis',
        'author_email': 'mikatammi@gmail.com',
        'version': '0.1',
        'requires': ['nose'],
        'provides': ['foreperiodanalysis'],
        'scripts': []
}

setup(**config)
