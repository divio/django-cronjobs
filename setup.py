APP_NAME = 'cronjobs'
PACKAGE_NAME = 'django-%s' % APP_NAME
DESCRIPTION = 'django cronjobs app'
PROJECT_URL = 'http://github.com/divio/%s/' % PACKAGE_NAME

INSTALL_REQUIRES = [
        #'django (>1.1.0)',
        #'django-tinymce',
        #'django-tagging',
    ]
AUTHOR="Patrick Lauber"

EXTRA_CLASSIFIERS = [
]

#VERSION = __import__(APP_NAME).__version__
VERSION = '0.1.0'

# DO NOT EDIT ANYTHING DOWN HERE... this should be common to all django app packages
from setuptools import setup, find_packages
import os



classifiers = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]
if not 'a' in VERSION and not 'b' in VERSION: classifiers.append('Development Status :: 5 - Production/Stable')
elif 'a' in VERSION: classifiers.append('Development Status :: 3 - Alpha')
elif 'b' in VERSION: classifiers.append('Development Status :: 4 - Beta')

for c in EXTRA_CLASSIFIERS:
    if not c in classifiers:
        classifiers.append(c)

def read(fname):
    # read the contents of a text file
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    author=AUTHOR,
    name=PACKAGE_NAME,
    version=VERSION,
    url=PROJECT_URL,
    description=DESCRIPTION,
    long_description=read('README.rst') + '\n\n\n' + read('HISTORY'),
    platforms=['OS Independent'],
    classifiers=classifiers,
    requires=INSTALL_REQUIRES,
    packages=find_packages(),
    zip_safe = False
)