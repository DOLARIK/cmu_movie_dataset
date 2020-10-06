from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

# with open('LICENSE') as f:
#     license = f.read()

setup(
    name='cmu_movie_dataset',
    version='0.1.1',
    description='For loading CMU Movie Dataset in python',
    long_description=readme,
    author='Divyanshu Gupta',
    author_email='divyanshu30gupta@gmail.com',
    url='https://github.com/DOLARIK/cmu_movie_dataset',
    # license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

    