from setuptools import setup, find_packages
with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='markdown-customblocks',
    version='1.4.1',
    keywords='markdown extension customblocks admonitions container figure map youtube vimeo twitter facebook instagram verkami goteo mastodon wikipedia peertube',
    description='Python Markdown extension to add custom parametrizable and nestable blocks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='David García Garzón',
    author_email='voki@canvoki.net',
    python_requires='>=3.8',
    url='https://vokimon.github.io/markdown-customblocks',
    packages=find_packages(exclude=['test*']),
    entry_points={
        'markdown.extensions': [
            'customblocks = customblocks:CustomBlocksExtension',
        ],
        'markdown.customblocks.generators': [
            'attention = customblocks.generators:admonition',
            'caution = customblocks.generators:admonition',
            'danger = customblocks.generators:admonition',
            'error = customblocks.generators:admonition',
            'hint = customblocks.generators:admonition',
            'important = customblocks.generators:admonition',
            'note = customblocks.generators:admonition',
            'tip = customblocks.generators:admonition',
            'warning = customblocks.generators:admonition',
            'youtube = customblocks.generators:youtube',
            'peertube = customblocks.generators:peertube',
            'vimeo = customblocks.generators:vimeo',
            'verkami = customblocks.generators:verkami',
            'goteo = customblocks.generators:goteo',
            'mastodon = customblocks.generators:mastodon',
            'twitter = customblocks.generators:twitter',
            'facebook = customblocks.generators:facebook',
            'instagram = customblocks.generators:instagram',
            'map = customblocks.generators:map',
            'linkcard = customblocks.generators:linkcard',
            'figure = customblocks.generators:figure',
            'wikipedia = customblocks.generators:wikipedia',
        ],
    },
    install_requires=[
        'markdown',
        'yamlns>=0.11', # supports assertNsContains
        'beautifulsoup4',
        'decorator',
        'geocoder', # map
        'pytest', # testing
        'pytest-cov<4', # testing
        'responses', # testing
        #'mkdocs', # docs
        #'mkdocs-material', # docs
        'urllib3<2', # conflicts with requests
        'python-magic', # figure embed
        'pillow',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    project_urls={
        "Documentation": 'https://vokimon.github.io/markdown-customblocks',
        "Code": 'https://github.com/vokimon/markdown-customblocks',
    },
)

# vim: et ts=4 sw=4
