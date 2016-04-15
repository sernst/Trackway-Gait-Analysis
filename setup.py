from setuptools import setup

setup(
    name='tracksim',
    version='0.1',
    description='Trackway Gait Analysis Toolkit',
    url='https://github.com/sernst/Trackway-Gait-Analysis',
    author='Scott Ernst',
    author_email='swernst@gmail.com',
    license='MIT',
    packages=['tracksim'],
    zip_safe=False,
    install_requires=[
        'measurement_stats',
        'plotly',
        'pandas',
        'boto3',
        'numpy',
        'six'
    ]
)
