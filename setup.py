from setuptools import setup, find_packages

setup(
    name = "homepagebuilder",
    version = "0.14.0",
    author = "Nattiden",
    author_email = "lightbeacon@bugjump.net",
    url = "https://github.com/Light-Beacon/HomepageBuilder",
    description = "A tool to generate homepage code for PCL2",
    keywords = ['PCL'],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: GNU Affero General Public License v3',
    'Natural Language :: Chinese (Simplified)',
    'Natural Language :: English',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.9',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],

    packages = find_packages(where="src"),
    package_dir = {"":"src"},
    include_package_data=True,
    license='AGPL-3.0',
    #data_files = [('src/resources', ['src/resources'])],
    entry_points = {
        'console_scripts': [
            'builder = main:main'
        ]
    }
)