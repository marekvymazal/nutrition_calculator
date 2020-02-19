from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='nutrition_calculator',
   version='0.1',
   description='Calculates nutrition data and costs of recipes.',
   long_description=long_description,
   author='Marek Vymazal',
   packages=['nutrition_calculator'],  #same as name
   install_requires=['pandas'], #external packages as dependencies
   entry_points={
          'console_scripts': [
              'nutrition_calculator = nutrition_calculator.__main__:main'
          ]
      },
)
