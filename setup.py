from setuptools import find_packages, setup
from typing import List

def get_requirements( filename: str) -> List[str]:
    '''
    the function will return list of requirements
    ''' 
    package_list = []
    with open(filename, 'r') as file_obj:
        pkg_names = file_obj.readlines()
        for name in pkg_names:
            package_list.append(name.replace('\n', ''))
            
    if "-e ." in package_list : package_list.remove('-e .')
    return package_list

setup(
    name="job-lead-generator",
    version='0.0.1',
    author='nilesh singh',
    author_email='nileshsingh2021fybsc@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
