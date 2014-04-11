from setuptools import setup

setup(
    name='github_observer',
    version='0.1',
    scripts=['scripts/github_observer.py'],
    zip_safe=False,
    install_requires=['PyGithub', 'pandas']
)

