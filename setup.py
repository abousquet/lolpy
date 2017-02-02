from setuptools import setup

setup(name='lolpy',
      version='0.1',
      description='Python 3 Package for Interaction with the League of Legends API',
      url='https://github.com/abousquet/lolPy',
      author='Adam Bousquet',
      license='MIT',
      packages=['lolpy'],
      zip_safe=False,
      install_requires=["lolpy==0.1",
                        "numpy==1.12.0",
                        "requests==2.12.4"])