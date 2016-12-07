from setuptools import setup
from setuptools import find_packages

setup(
    name='tracksim',
    version='0.1.1',
    description='Trackway Gait Analysis Toolkit',
    url='https://github.com/sernst/Trackway-Gait-Analysis',
    author='Scott Ernst',
    author_email='swernst@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',

        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    install_requires=[
        'measurement_stats',
        'plotly',
        'pandas',
        'boto3',
        'numpy',
        'six',
        'jinja2',
        'markdown'
    ],
    entry_points=dict(
            console_scripts=[
                'tracksim=tracksim.scripts.tracksim_cli:run'
            ]
        )
)
