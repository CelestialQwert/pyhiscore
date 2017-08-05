from setuptools import setup

setup(
    name='pyhiscore',
    packages=['pyhiscore'],
    include_package_data=True,
    install_requires=[
        'flask','wtforms'
    ],
)