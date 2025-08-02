from setuptools import setup, find_packages

setup(
    name = "homepagebuilder",
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    author = "Nattiden",
    author_email = "lightbeacon@bugjump.net",
    url = "https://github.com/Light-Beacon/HomepageBuilder",
    description = "A tool to generate homepage code for PCL2",
    keywords = ['PCL'],
    classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: GNU Affero General Public License v3',
    'Natural Language :: Chinese (Simplified)',
    'Natural Language :: English',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.9',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'beautifulsoup4>=4.12.3',
        'Markdown>=3.5.2',
        'PyYAML>=6.0.1',
        'flask>=3.0.3'
    ],
    packages = find_packages(where="src"),
    package_dir = {"":"src"},
    include_package_data=True,
    license='AGPL-3.0',
    entry_points = {
        'console_scripts': [
            'builder = homepagebuilder.main:main'
        ]
    }
)