from setuptools import setup

setup(
    name='pyhiscore',
    version='0.0.0.0.1',
    author="Eric Buzan",
    author_email="eric.buzan@gmail.com",
    url='https://github.com/ericbuzan/pyhiscore',
    description='multi-game hi score tracker',
    packages=['pyhiscore'],
    install_requires=[
        'flask','wtforms'
    ],
)