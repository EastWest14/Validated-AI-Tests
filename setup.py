from setuptools import setup, find_packages

setup(
    name='validated_ai_tests',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # 'dependency1>=1.0',
    ],
    author='Andrew Prosikhin',
    author_email='aprosikhin@gmail.com',
    description='Automated tests for complex Gen AI outputs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/EastWest14/Validated-AI-Tests',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
