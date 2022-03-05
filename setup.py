from setuptools import setup, find_packages
with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='markdown-customblocks',
    version='1.1.4',
    keywords='markdown extension customblocks admonitions container figure youtube vimeo twitter verkami goteo',
    description='Python Markdown extension to add custom parametrizable and nestable blocks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='David García Garzón',
    author_email='voki@canvoki.net',
    python_requires='>=2.7',
    url='https://github.com/vokimon/markdown-customblocks',
    packages=find_packages(exclude=['test*']),
    entry_point={
        'markdown.extensions': [
            'customblocks = customblocks:CustomBlocksExtension',
        ]
    },
    install_requires=[
        'markdown',
        'yamlns',
        'beautifulsoup4',
        'decorator',
        'pytest', # testing
        'responses', # testing
    ],
    test_suite='customblocks',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',
    ]
)

# vim: et ts=4 sw=4
