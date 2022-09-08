from setuptools import setup
from jhsiao.namespace import make_ns
make_ns('jhsiao')
setup(
    name='jhsiao-pdb',
    version='0.0.1',
    author='Jason Hsiao',
    author_email='oaishnosaj@gmail.com',
    description='monkey patched pdb',
    packages=['jhsiao'],
    py_modules=['jhsiao.pdb']
)
