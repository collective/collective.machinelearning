from setuptools import setup, find_packages
import os

version = '1.0.dev0'

setup(
    name='collective.machinelearning',
    version=version,
    description="Machine learning tools",
    long_description=open("README.txt").read() + "\n" +
    open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='plone',
    author='Ramon Navarro Bosch',
    author_email='',
    url='https://github.com/collective/collective.machinelearning',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.app.dexterity',
        'plone.namedfile [blobs]',
        # -*- Extra requirements: -*-
        'plone.behavior',
        'zope.schema',
        'zope.interface',
        'zope.component',
        # -*- machine learning -*-
        # -*- see also http://scikit-learn.org/stable/install.html -*-
        'scikit-learn',
        'nltk',
    ],
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
