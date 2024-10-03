from setuptools import setup, find_packages

setup(
    name='pytest-vtestify',
    version='0.1.0',
    author='Aria Suseno',
    author_email='idejongkok@gmail.com',
    description='A pytest plugin for visual assertion using SSIM and image comparison.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/idejongkok/pytest-vtestify',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'opencv-python',
        'scikit-image',
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Pytest',
    ],
    python_requires='>=3.6',
    entry_points={
        'pytest11': [
            'vtestify = visual_testify.visual_assertion',
        ]
    }
)
