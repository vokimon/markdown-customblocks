from setuptools import setup, find_packages
with open('README.md') as readme:
	long_description = readme.read()

setup(
    name='markdown-customblocks',
    version='0.0.0',
    keywords='markdown extension customblocks admonitions container youtube twitter',
    description='Extension pack for Python Markdown.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='David García Garzón',
    author_email='voki@canvoki.net',
    python_requires='>=2.7',
    url='https://github.com/vokimon/markdown-customblocks',
    packages=find_packages(exclude=['test*']),
    install_requires=[
		'markdown',
		'nose',
		'rednose',
	],
    license='MIT License',
	test_suite='nose.collector',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
		'Intended Audience :: Other Audience'
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)'
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