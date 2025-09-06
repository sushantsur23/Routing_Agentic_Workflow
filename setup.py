# from setuptools import find_packages, setup

# setup(
#     name = 'AI Marketing Campaign Generator',
#     version= '0.0.0',
#     author= 'Sushant Sur',
#     author_email= 'sushant.sur23@gmail.com',
#     packages= find_packages(),
#     install_requires = []

# )

#Run command Pip install .

from setuptools import find_packages, setup
from pathlib import Path

# Read the requirements from requirements.txt
def get_requirements():
    requirements_path = Path(__file__).parent / 'requirements.txt'
    with open(requirements_path, 'r') as f:
        requirements = f.read().splitlines()
        # Remove empty lines and comments
        requirements = [req.strip() for req in requirements 
                       if req.strip() and not req.startswith('#')]
    return requirements

setup(
    name='AI Marketing Campaign Generator',
    version='0.0.0',
    author='Sushant Sur',
    author_email='sushant.sur23@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
    # Optional: Include additional metadata
    description='An AI-powered marketing campaign generator',
    long_description=open('README.md').read() if Path('README.md').exists() else '',
    long_description_content_type='text/markdown',
    url='https://github.com/sushantsur23/Routing_Agentic_Workflow',  # Update with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)